from application.models import Venue,User
from application.models import Show,Userbooking,Rating
from app import cache

@cache.cached(timeout=120,key_prefix = 'get_all_users')
def get_all_users():
    user = User.query.all()
    return user

@cache.cached(timeout=120,key_prefix = 'get_all_venues')
def get_all_venues():
    venue = Venue.query.all()
    return venue

@cache.memoize(120)
def get_venues_by_admin(num):
    venue = Venue.query.filter_by(admin_no = num).all()
    return venue

@cache.memoize(120)
def get_venues_by_list(num):
    venue = Venue.query.filter_by(venue_no = num).first()
    return venue

@cache.cached(timeout=120,key_prefix = 'get_all_shows')
def get_all_shows():
    show = Show.query.all()
    return show

@cache.cached(timeout=120,key_prefix = 'get_all_bookings')
def get_all_bookings():
    ub = Userbooking.query.all()
    return ub

@cache.memoize(5)
def get_bookings_by_user(num):
    ub = Userbooking.query.filter_by(user_no = num).all()
    return ub

@cache.memoize(5)
def get_bookings_by_show(num):
    ub = Userbooking.query.filter_by(show_no = num).all()
    return ub

@cache.cached(timeout=120,key_prefix = 'get_all_ratings')
def get_all_ratings():
    ratings = Rating.query.all()
    return ratings

@cache.memoize(5)
def get_ratings_by_user(num):
    ratings = Rating.query.filter_by(user_no = num).all()
    return ratings

@cache.memoize(5)
def get_ratings_by_show(num):
    ratings = Rating.query.filter_by(show_no = num).all()
    return ratings

