
from config import db

class Acc(db.Model):
    __tablename__ = "account"
    id = db.Column('acc_id', db.Integer , primary_key=True)
    type = db.Column('acc_type', db.Integer)
    username = db.Column('username', db.String(), unique=True, index=True)
    password = db.Column('password', db.String())
    email = db.Column('email', db.String(), unique=True, index=True)
    image_file = db.Column('img', db.String(), nullable=False, default='default.png')

    def __init__(self, username, password, email):
        self.username = username
        self.type = 0;
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_admin(self):
        return type == 1

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Acc %r>' % (self.username)

class User(db.Model):
    __tablename__ = "user_acc"
    id = db.Column('user_id', db.Integer , primary_key=True)
    fname = db.Column('fname', db.String())
    lname = db.Column('lname', db.String())
    contact = db.Column('contact', db.String())

    def __init__(self, id, fname, lname, contact):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.contact = contact

class Admin_acc(db.Model):
    __tablename__ = "admin_acc"
    id = db.Column('admin_id', db.Integer , primary_key=True)
    college = db.Column('college_id', db.Integer , primary_key=True)
    fname = db.Column('fname', db.String())
    lname = db.Column('lname', db.String())
    contact = db.Column('contact', db.String())

    def __init__(self, id, fname, lname, college, contact):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.college = COLLEGENAMES.get(college, 1)
        self.contact = contact

class Venue(db.Model):
    __tablename__ = "venue"
    id = db.Column('venue_id', db.Integer , primary_key=True)
    college = db.Column('college_id', db.Integer , primary_key=True)
    name = db.Column('venue_name', db.String())
    capacity = db.Column('capacity', db.Integer())
    rate = db.Column('rate', db.Integer)
    equipment = db.Column('equipment', db.String())
    image_file = db.Column('venue_img', db.String(), nullable=False)

    def __init__(self, name, college, capacity, rate, equipment, image_file):
        self.name = name
        self.college = college
        self.capacity = capacity
        self.rate = rate
        self.equipment = equipment
        self.image_file = image_file

    def get_id(self):
        return unicode(self.id)

class College(db.Model):
    __tablename__ = "college"
    id = db.Column('college_id', db.Integer , primary_key=True)
    name = db.Column('college_name', db.String())
    abb = db.Column('college_abb', db.String())
    img = db.Column('college_img', db.String(), nullable=False)

    def __init__(self, name, abb):
        self.id = id
        self.name = name
        self.abb = abb

class Events(db.Model):
    __tablename__ = "events"
    organizer = db.Column('organizer_id', db.Integer)
    venue = db.Column('venue_id', db.Integer)
    id = db.Column('event_id', db.Integer , primary_key=True)
    title = db.Column('event_name', db.String())
    description = db.Column('event_desc', db.String())
    tags = db.Column('event_tags', db.String())
    date_s = db.Column('event_date', db.Date())
    date_e = db.Column('event_date2', db.Date(), nullable=True)
    start = db.Column('event_time_s', db.Time())
    end = db.Column('event_time_e', db.Time())
    partnum = db.Column('expected_participants', db.Integer())
    status = db.Column('event_status', db.String())
    comment = db.column('event_comment', db.String())
    image_file = db.Column('event_img', db.String(), nullable=False)

    def __init__(self, organizer, venue, title, description, tags, date_s, date_e, start, end, partnum, status, comment, image_file ):
        self.organizer = organizer
        self.title = title
        self.description = description
        self.venue = venue
        self.tags = tags
        self.date_s = date_s
        self.date_e = date_e
        self.start = start
        self.end = end
        self.partnum = partnum
        self.status = status
        self.comment = comment
        self.image_file = image_file




