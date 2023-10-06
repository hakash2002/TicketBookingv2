from datetime import datetime, time
from flask import send_file
import csv
import os
import shutil
from jinja2 import Environment, FileSystemLoader
from celery.schedules import crontab
from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity)
import time
import matplotlib.pyplot as plt
from json import dumps
from httplib2 import Http
from sqlalchemy import func
from flask_bcrypt import Bcrypt
from application.database import db
from flask import current_app as app
from application.models import User, Venue, Admin, Show
from application.models import Userbooking, Rating
from celery.result import AsyncResult
from app import celery, cache
import data_access
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
bcrypt = Bcrypt(app)
SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025


@celery.task()
def generate_csv(venueid):
    time.sleep(6)
    venue = Venue.query.filter_by(venue_no=venueid).all()
    cache.delete('get_venues_by_list')
    name = data_access.get_venues_by_list(venueid).name
    vname = "".join(name.split())
    shows_filled = {}
    static_folder = os.path.join(app.root_path, 'static')
    csv_file_path = os.path.join(static_folder, f'{vname}.csv')
    for i in venue:
        for j in i.shows:
            shows_filled[j.show_no] = 0
    for i in shows_filled.keys():
        ub = data_access.get_bookings_by_user(i)
        if ub:
            for k in ub:
                shows_filled[i] += k.quantity
        else:
            pass
    csv_data = f"venuename,{name}\n"
    csv_data += "Show Name,Number of Bookings,No of unfilled,Capacity,Price of single ticket,Rating,Price,Revenue from this show\n"
    for i in venue:
        for j in i.shows:
            showname = j.name
            noofbookings = shows_filled[j.show_no]
            noofunfilled = int(i.capacity) - int(noofbookings)
            capacity = i.capacity
            price = j.price
            revenue = price * noofbookings
            rating = j.rate
            csv_data += f"{showname},{noofbookings},{noofunfilled},{capacity},{price},{rating},{price},Rs:{revenue}\n"

    # Write CSV content to file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_file.write(csv_data)

    return csv_file_path


@app.route("/openfile/<id>")
def openfile(id):
    try:
        path = os.path.join(app.root_path, "static", f"{id}.csv")
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        return "CSV file not found", 404


@celery.on_after_configure.connect
def set_up_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18, minute=0),  # Schedule at 6:00 PM
        senduserremainder.s(),
        name="daily_remainder"
    )
    sender.add_periodic_task(
        crontab(0, 0, day_of_month='30'),  # Schedule at 6:00 PM
        send_email_to_all.s(),
        name="email"
    )


@celery.task()
def senduserremainder():
    from datetime import time
    users = data_access.get_all_users()
    current_time = datetime.now().time()

    for user in users:
        print(user.timestamp.date() < datetime.now().date())
        if user.timestamp.date() < datetime.now().date():
            if current_time >= time(18, 0):
                send_chat_message(
                    f"Reminder: Hey check out whats new today, {user.username}!")


def send_chat_message(message):
    url = "https://chat.googleapis.com/v1/spaces/AAAADetZD7M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ydmiZlqIWEe27iFW4LSEPPIhO9ptv4s7UEQ56Sj71bc"
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    app_message = {
        'text': message
    }
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(app_message),
    )


def send_email(to_address, subject, email_content):
    SENDER_ADDRESS = "bookmytickets.net"
    SENDER_PASSWORD = ""
    # Create a MIMEText object for the email content
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    # Attach the HTML message to the email
    msg.attach(MIMEText(email_content, "html"))

    # Connect to the SMTP server and send the email
    try:
        smtp = smtplib.SMTP(SMPTP_SERVER_HOST, SMPTP_SERVER_PORT)
        smtp.login(SENDER_ADDRESS, SENDER_PASSWORD)
        smtp.sendmail(SENDER_ADDRESS, to_address, msg.as_string())
        smtp.quit()
        print(f"Email sent successfully to: {to_address}")
        return True
    except Exception as e:
        print(f"Failed to send email to: {to_address}")
        print(f"Error: {str(e)}")
        return False


@celery.task()
def send_email_to_all():
    user = data_access.get_all_users()
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    subject = "Monthly Report"
    for u in user:
        template_name = "monthlyreport.html"
        template = env.get_template(template_name)
        content = monthlyreport(u.user_no)
        message = template.render(context=content, username=u.username)
        send_email(u.email, subject, message)
    return "email should arrive shortly..."


def monthlyreport(userno):
    user = User.query.filter_by(user_no=userno).first()
    context = []
    ub = data_access.get_bookings_by_user(user.user_no)
    cache.delete('get_all_shows')
    Shows = data_access.get_all_shows()
    venue = data_access.get_all_venues()
    for i in ub:
        dict = {}
        dict["movie_title"] = Shows[i.show_no-1].name
        dict["venuename"] = venue[Shows[i.show_no-1].venue_no-1].name
        datestring = i.timestamp.date().strftime("%d-%m-%Y")
        dict["booking_date"] = datestring
        timestring = i.timestamp.time().strftime("%H:%M:%S")
        dict["booking_time"] = timestring
        dict["num_tickets"] = i.quantity
        dict["total_amount"] = int(i.quantity)*int(Shows[i.show_no-1].price)
        context.append(dict)
    return context


@app.route("/trigger-celery-job/<id>")
def trigger_celery_job(id):
    a = generate_csv.delay(id)
    return {
        "Task_ID": a.id,
        "Task_State": a.state,
        "Task_Result": a.result
    }


@app.route("/status/<id>")
def checkstatus(id):
    res = AsyncResult(id, app=celery)
    return {
        "Task_ID": res.id,
        "Task_State": res.state,
        "Task_Result": res.result
    }

# ----------------------STARTS-------------------------------


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    userid = data["userid"]
    password = data["password"]
    hashed_pwd = bcrypt.generate_password_hash(password)
    username = data["username"]
    email = data["email"]
    user = User.query.filter_by(id=userid).first()
    if user:
        return jsonify({'message': 'Username already exists try again'}), 402
    else:
        try:
            user1 = User(id=userid, password=hashed_pwd,
                         username=username, email=email)
            db.session.add(user1)
            db.session.commit()
            access_token = create_access_token(identity=user1.id)
            return jsonify({'message': 'Successfully created an account', 'userusername': user1.username, 'access_token': access_token})
        except:
            return jsonify({'message': 'Not successfull'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data["user_id"]
    password = data["password"]
    user = User.query.filter_by(id=user_id).first()
    user.timestamp = datetime.now()
    db.session.commit()
    if user:
        if bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login successful', 'userusername': user.username, 'access_token': access_token})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'message': 'Check Userid'}), 405


@app.route('/shows', methods=['GET'])
@jwt_required()
def userdash():
    current_user_id = get_jwt_identity()
    user_data = User.query.filter_by(id=current_user_id).first()
    if user_data and request.method == 'GET':
        return jsonify({'user': user_data.id, 'password': user_data.password}), 200
    else:
        return jsonify({'message': 'not found'}), 403


@app.route('/movies', methods=['GET', 'POST'])
@jwt_required()
def movielist():
    current_user_id = get_jwt_identity()
    user_data = User.query.filter_by(id=current_user_id).first()
    admin = Admin.query.filter_by(id=current_user_id).first()
    if user_data or admin:
        cache.delete('get_all_shows')
        movies = data_access.get_all_shows()
        ub = data_access.get_all_bookings()
        seats = {}
        dates = []
        for i in movies:
            seats[i.show_no] = data_access.get_venues_by_list(
                i.venue_no).capacity
            formatted_date = i.date
            if formatted_date not in dates:
                dates.append(formatted_date)
        for i in ub:
            if i.show_no in seats:
                seats[i.show_no] -= i.quantity
        return jsonify([{'id': movie.show_no, 'name': movie.name, 'price': movie.price, 'rate': movie.rate, 'tags': movie.tags.split(","), 'seatsavailable': seats[movie.show_no], 'venue_no':movie.venue_no, 'starttime':movie.start_time, 'endtime': movie.end_time, 'tag':movie.tags, 'date': movie.date} for movie in movies])
    else:
        return jsonify({'message': 'login again'})


@app.route('/theatres', methods=['GET', 'POST'])
@jwt_required()
def theatrelist():
    current_user_id = get_jwt_identity()
    user_data = User.query.filter_by(id=current_user_id).first()
    if user_data:
        try:
            cache.delete('get_all_venues')
            venues = data_access.get_all_venues()
            return jsonify([{'id': venue.venue_no, 'name': venue.name, 'place': venue.place, 'location': venue.location, 'shows': [{"venueid": venue.venue_no, "showid": i.show_no, "showname": i.name.lower(), "showdate": i.date} for i in venue.shows], 'combined': venue.name + ' ' + venue.location + ' ' + venue.place, 'capacity': venue.capacity} for venue in venues])
        except:
            return jsonify({'message': 'error feching theatres'})

    else:
        return jsonify({'message': 'login again'})


@app.route('/booking', methods=['POST'])
@jwt_required()
def ticketsbooking():
    current_user_id = get_jwt_identity()
    user_data = User.query.filter_by(id=current_user_id).first()
    if user_data:
        try:
            data = request.get_json()
            show_no = data["mid"]
            quantity = data["counter"]
            userbooking = Userbooking(
                user_no=user_data.user_no, show_no=show_no, quantity=quantity)
            db.session.add(userbooking)
            db.session.commit()
            return jsonify({'message': 'successfull'}), 200
        except:
            return jsonify({'message': 'not successfull'})
    else:
        jsonify({'message': 'Unauthorized'})


@app.route('/userbooking', methods=['GET'])
@jwt_required()
def userbookings():
    current_user_id = get_jwt_identity()
    user_data = User.query.filter_by(id=current_user_id).first()
    if user_data:
        venue = data_access.get_all_venues()
        show = data_access.get_all_shows()
        rated = {}
        cache.delete('get_all_ratings')
        cache.delete('get_all_bookings')
        cache.delete('get_bookings_by_user')
        cache.delete('get_ratings_by_user')
        rate = data_access.get_ratings_by_user(user_data.user_no)
        ub = data_access.get_bookings_by_user(user_data.user_no)
        for i in ub:
            rated[i.show_no] = False
        for i in rate:
            rated[i.show_no] = True
        return jsonify([{'show_name': show[i.show_no-1].name, 'venue_name':venue[show[i.show_no-1].venue_no-1].name, 'start_time':show[i.show_no-1].start_time, 'quantity': i.quantity, 'show_no':i.show_no, 'location': venue[show[i.show_no-1].venue_no-1].place + ', ' + venue[show[i.show_no-1].venue_no-1].location, 'rated':rated[i.show_no], 'date': datetime.strptime(show[i.show_no-1].date, '%Y-%m-%d').strftime('%d/%m/%Y')} for i in ub])
    else:
        jsonify({'message': 'Unauthorized'}), 401


@app.route('/rate', methods=['POST'])
@jwt_required()
def rate():
    current_user_id = get_jwt_identity()
    user_data = User.query.filter_by(id=current_user_id).first()
    if user_data:
        try:
            data = request.get_json()
            rate = float(data["rate"])
            show = int(data["show"])
            rating = Rating(user_no=user_data.user_no,
                            show_no=show, rating=rate)
            db.session.add(rating)
            return jsonify({'message': 'successfull'})
        except:
            return jsonify({'message': 'rating successfull'})
        finally:
            db.session.commit()
            show = Show.query.filter_by(show_no=show).first()
            shownames = Show.query.filter_by(name=show.name).all()
            L = []
            for i in shownames:
                L.append(i.show_no)
            cache.delete('get_all_ratings')
            rating = data_access.get_all_ratings()
            count = 0
            rateval = 0
            for i in rating:
                if i.show_no in L:
                    count += 1
                    rateval += i.rating
            for i in shownames:
                if count != 0:
                    i.rate = round(rateval/count, 2)
            db.session.commit()

    else:
        jsonify({'message': 'Unauthorized'})

# ------------------------ADMIN END----------------------------------


@app.route('/admin/register', methods=['POST'])
def adminregister():
    data = request.get_json()
    admin_id = data["adminid"]
    password = data["password"]
    hashed_pwd = bcrypt.generate_password_hash(password)
    print(hashed_pwd)
    admin = Admin.query.filter_by(id=admin_id).first()
    if not admin:
        try:
            admin = Admin(id=admin_id, password=hashed_pwd)
            db.session.add(admin)
            db.session.commit()
            access_token = create_access_token(identity=admin.id)
            return jsonify({'message': 'Signup successful', 'username': admin.id, 'access_token': access_token})
        except:
            return jsonify({'message': 'Error creating account'}), 403
    else:
        return jsonify({'message': 'AdminId already exists'}), 402


@app.route('/admin/login', methods=['POST'])
def adminlogin():
    data = request.get_json()
    admin_id = data["adminid"]
    password = data["password"]
    admin = Admin.query.filter_by(id=admin_id).first()
    if admin:
        if bcrypt.check_password_hash(admin.password, password):
            access_token = create_access_token(identity=admin.id)
            return jsonify({'message': 'Login successful', 'username': admin.id, 'access_token': access_token})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'message': 'Check Adminid'}), 405


@app.route('/admin/venues', methods=['GET'])
@jwt_required()
def venuesget():
    current_user_id = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user_id).first()
    if admin:
        venues = Venue.query.filter_by(admin_no=admin.admin_no).all()
        return jsonify([{'id': venue.venue_no, 'venuename': venue.name, 'shows': [{'id': i.show_no, 'showname': i.name, 'date': i.date} for i in venue.shows], 'location': venue.location, 'place': venue.place, 'capacity': venue.capacity} for venue in venues])
    else:
        return jsonify({'message': 'login again'})


@app.route('/admin/createvenue', methods=['POST'])
@jwt_required()
def createvenues():
    data = request.get_json()
    vname = data["vname"].capitalize()
    vlocation = data["vlocation"].capitalize()
    vplace = data["vplace"].capitalize()
    vcapacity = data["vcapacity"]
    current_user_id = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user_id).first()
    if admin:
        venue = Venue(name=vname, location=vlocation,
                      capacity=vcapacity, place=vplace, admin_no=admin.admin_no)
        try:
            db.session.add(venue)
            db.session.commit()
            return jsonify({'message': 'Successfullly Created Venue'})
        except:
            return jsonify({'message': 'Error creating venue'})
    else:
        return jsonify({'message': 'Invalid Credentials'})


@app.route('/admin/updatevenue', methods=['PUT'])
@jwt_required()
def updatevenue():
    data = request.get_json()
    vid = data["vid"]
    vname = data["vname"].capitalize()
    vlocation = data["vlocation"].capitalize()
    vplace = data["vplace"].capitalize()
    vcapacity = data["vcapacity"]
    current_user_id = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user_id).first()
    if admin:
        venue = Venue.query.filter_by(venue_no=vid).first()
        venue.name = vname
        venue.location = vlocation
        venue.place = vplace
        venue.capacity = vcapacity
        try:
            db.session.commit()
            return jsonify({'message': 'Successfullly Updated Venue'})
        except:
            db.session.rollback()
            return jsonify({'message': 'Error updating venue'})
    else:
        return jsonify({'message': 'Invalid Credentials'})


@app.route('/admin/createshow', methods=['POST'])
@jwt_required()
def createshows():
    data = request.get_json()
    sname = data["sname"].capitalize()
    stags = data["stags"].capitalize()
    srating = data["srating"]
    sstime = data["sstime"]
    setime = data["setime"]
    sprice = data["sprice"]
    vid = data["vid"]
    sdate = data["sdate"]
    current_user_id = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user_id).first()
    if admin:
        show = Show(name=sname, rate=srating, tags=stags, price=sprice,
                    admin_no=admin.admin_no, venue_no=vid, start_time=sstime, end_time=setime, date=sdate)
        try:
            db.session.add(show)
            db.session.commit()
            return jsonify({'message': 'Successfullly Created Show'})
        except:
            return jsonify({'message': 'Error creating Show'})

    else:
        return jsonify({'message': 'Invalid Credentials'})


@app.route('/admin/updateshow', methods=['PUT'])
@jwt_required()
def updateshows():
    data = request.get_json()
    sname = data["sname"].capitalize()
    stags = data["stags"].capitalize()
    srating = data["srating"]
    sstime = data["sstime"]
    sentime = data["setime"]
    sprice = data["sprice"]
    vid = data["vid"]
    sid = data["sid"]
    current_user_id = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user_id).first()

    if admin:
        show = Show.query.filter_by(show_no=sid).first()
        beforename = show.name
        showa = Show.query.filter_by(name = beforename).all()
        image_directory = os.path.join(
            '/home/hakash2002/Documents/mad2project', 'my-custom', 'src', 'assets', 'images')
        beforeimg = os.path.join(image_directory, beforename + '.jpg')
        afterimg = os.path.join(image_directory, sname + '.jpg')
        if len(showa) > 1:
            print(beforename)
            shutil.copy2(beforeimg, afterimg)
        else:
            shutil.move(beforeimg, afterimg)
        show.name = sname
        show.rate = srating
        show.tags = stags
        show.price = sprice
        show.admin_no = admin.admin_no
        show.venue_no = vid
        show.start_time = sstime
        show.end_time = sentime
        try:
            db.session.commit()

            return jsonify({'message': 'Successfullly Updated Show'})
        except:
            db.session.rollback()
            return jsonify({'message': 'Error updating Show'})
    else:
        return jsonify({'message': 'Invalid Credentials'})


@app.route('/admin/deleteshow', methods=['DELETE'])
@jwt_required()
def deleteshow():
    current_user_id = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user_id).first()
    data = request.get_json()
    show_no = int(data["sid"])
    if admin:
        show = Show.query.filter_by(show_no=show_no).first()
        ub = data_access.get_bookings_by_show(show_no)
        if show:
            if ub == []:
                rating = data_access.get_ratings_by_show(show_no)
                for k in rating:
                    db.session.delete(k)
                    db.session.commit()
                db.session.delete(show)
                db.session.commit()
                num = int(show_no)
                max_id = int(db.session.query(
                    func.max(Show.show_no)).scalar())
                for i in range(num, max_id):
                    ub = data_access.get_bookings_by_show(i+1)
                    show = Show.query.filter_by(show_no=i+1).first()
                    rt = data_access.get_ratings_by_show(i+1)
                    if ub != []:
                        for j in ub:
                            j.show_no = i
                    if rt != []:
                        for l in rt:
                            l.show_no = i
                    show.show_no = i
                try:
                    db.session.commit()
                
                except:
                    return jsonify({'message': 'Error deleting Show'})
            else:
                return jsonify({'message': 'Cant delete user has booking active for this show'})
    else:
        return jsonify({'message': 'Invalid Credentials'})


@app.route('/admin/deletevenue', methods=['DELETE'])
@jwt_required()
def deletevenue():
    data = request.get_json()
    venue_no = int(data["vid"])
    current_user_id = get_jwt_identity()
    venue = Venue.query.filter_by(venue_no=venue_no).first()
    admin = Admin.query.filter_by(id=current_user_id).first()

    if admin:
        if venue:
            for i in venue.shows:
                ub = data_access.get_bookings_by_show(i.show_no)
                if ub != None:
                    return jsonify({'message': 'Warning! Venue has show bookings'})
            for i in venue.shows:
                num = int(i.show_no)
                rating = data_access.get_ratings_by_show(num)
                for k in rating:
                    db.session.delete(k)
                db.session.delete(i)
                db.session.commit()
                max_id = int(db.session.query(func.max(Show.show_no)).scalar())
                for i in range(num, max_id):
                    ub = data_access.get_bookings_by_show(i+1)
                    show = Show.query.filter_by(show_no=i+1).first()
                    if ub != []:
                        for j in ub:
                            j.show_no = i
                    show.show_no = i
                    db.session.commit()
            num1 = int(venue_no)
            max_id1 = int(db.session.query(func.max(Venue.venue_no)).scalar())
            db.session.delete(venue)
            db.session.commit()
            for i in range(num1, max_id1):
                venue = Venue.query.filter_by(venue_no=i+1).first()
                for j in venue.shows:
                    j.venue_no = i
                venue.venue_no = i
                db.session.commit()

            return jsonify({'message': 'Successfully deleted'})
    else:
        return jsonify({'message': 'Invalid Credentials'})


@app.route('/uploadimage', methods=['POST'])
def uploadimg():
    image = request.files['image']
    moviename = request.form['moviename'].capitalize()
    try:
        if image:
            cache.delete('get_all_shows')
            assets_path = os.path.join(
                'my-custom/src/assets/images', f'{moviename}.jpg')
            image.save(assets_path)
            return jsonify({'message': 'Image uploaded successfully'}), 200
        else:
            return jsonify({'message': 'Image or movie name missing'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500
