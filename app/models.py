from app import db
from datetime import datetime
import random




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    pins = db.relationship('Register', backref='users', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name) 



class Register(db.Model):
    __tablename__ = 'generate'

    s_n = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pin = db.Column(db.String(140), unique=True, nullable=False)
    request_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, pin):
        self.pin = pin

    def __repr__(self):
        return '{}'.format(self.pin)
 


def random_digits(n):
    """ A function to generate random 15 digit number. where n is the number of Digits"""
    lower = 10**(n-1)
    upper = 10**n - 1
    return random.randint(lower, upper)


def twelve_digit_serial_no(id):
    """ The function create a 12 digit serial number from any number with less than 11 digits"""
    f = str(10**(11 - len(str(id))))
    twelve_digit_id = f + str(id)
    return int(twelve_digit_id)




def database_serial_no(twelve_digit_sn):
    db_id = int(twelve_digit_sn) - 10**11
    return db_id
