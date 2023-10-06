from application.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    user_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=True)
    id = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bookings = db.relationship('Userbooking', backref='user',lazy='subquery')


class Venue(db.Model):
    __tablename__ = 'venue'
    venue_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    place = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    admin_no = db.Column(db.Integer, db.ForeignKey(
        'admin.admin_no'), nullable=False)
    shows = db.relationship('Show', backref='venue',lazy='subquery')

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    venue = db.relationship('Venue', backref='admin',
                            cascade='all, delete-orphan',lazy='subquery')


class Show(db.Model):
    __tablename__ = 'show'
    show_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    tags = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    venue_no = db.Column(db.Integer, db.ForeignKey(
        'venue.venue_no'), nullable=False)
    admin_no = db.Column(db.Integer, db.ForeignKey(
        'admin.admin_no'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    ratings = db.relationship('Rating', backref='show', lazy='subquery')
    rate = db.Column(db.Float, nullable=True)
    date = db.Column(db.String,nullable = False)



class Userbooking(db.Model):
    __tablename__ = 'userbooking'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_no = db.Column(db.Integer, db.ForeignKey(
        'user.user_no'), nullable=False)
    show_no = db.Column(db.Integer, db.ForeignKey(
        'show.show_no'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_no = db.Column(db.Integer, db.ForeignKey(
        'user.user_no'), nullable=False)
    show_no = db.Column(db.Integer, db.ForeignKey(
        'show.show_no'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

