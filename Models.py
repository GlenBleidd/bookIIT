
from config import db

COLLEGENAMES = {
    'MSU-IIT': 1,
    'College of Engineering': 2,
    'College of Science and Mathematics': 3,
    'College of Education': 4,
    'College of Arts and Social Science': 5,
    'College of Business Administration and Accountancy': 6,
    'College of Nursing': 7,
    'School of Computer Studies': 8,
    'Integrated Developmental School': 9,
    'PRISM': 10
}

COLLEGEID = {
    1: 'MSU-IIT',
    2: 'COE',
    3: 'CSM:',
    4: 'CED',
    5: 'CASS',
    6: 'CBAA',
    7: 'CON',
    8: 'SCS',
    9: 'IDS',
    10: 'PRISM'
}

class User(db.Model):
    __tablename__ = "user_acc"
    id = db.Column('acc_id', db.Integer , primary_key=True)
    type = db.Column('acc_type', db.Integer)
    username = db.Column('username', db.String(), unique=True, index=True)
    password = db.Column('password', db.String())
    email = db.Column('email', db.String(), unique=True, index=True)
    fname = db.Column('fname', db.String())
    lname = db.Column('lname', db.String())
    image_file = db.Column('img', db.String(), nullable=False, default='default.png')

    def __init__(self, username, password, email, fname, lname):
        self.username = username
        self.type = 0;
        self.password = password
        self.email = email
        self.fname = fname
        self.lname = lname

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

class Admin_acc(db.Model):
    __tablename__ = "admin_acc"
    id = db.Column('admin_id', db.Integer)
    faculty_id = db.Column('iit_faculty_id', db.String(), primary_key=True)
    college = db.Column('college_id', db.Integer)
    contact = db.Column('contact', db.String())

    def __init__(self, id, faculty_id, college, contact):
        self.id = id
        self.faculty_id = faculty_id
        self.college = COLLEGENAMES.get(college)
        self.contact = contact

class Venue(db.Model):
    __tablename__ = "venue"
    id = db.Column('venue_id', db.Integer , primary_key=True)
    college = db.Column('college_id', db.Integer , primary_key=True)
    name = db.Column('venue_name', db.String())
    capacity = db.Column('capacity', db.Integer())
    rate = db.Column('rate', db.Integer)
    equipment = db.Column('equipment', db.String())

    def __init__(self, name, college, capacity, rate, equipment):
        self.name = name
        self.college = COLLEGENAMES.get(college)
        self.capacity = capacity
        self.rate = rate
        self.equipment = equipment

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '{} - {}'.format(COLLEGEID.get(self.college), self.name)

class College(db.Model):
    __tablename__ = "college"
    id = db.Column('college_id', db.Integer , primary_key=True)
    name = db.Column('college_name', db.String())
    abb = db.Column('college_abb', db.String())

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
    start = db.Column('event_datetime_start', db.DateTime())
    end = db.Column('event_datetime_end', db.DateTime())
    status = db.Column('event_status', db.String())
    admin_comment = db.Column('admin_comment', db.String())

    def __init__(self, organizer, venue, title, description, tags, date, start, end, status ):
        self.organizer = organizer
        self.title = title
        self.description = description
        self.venue = venue
        self.tags = tags
        self.date = date
        self.start = start
        self.end = end
        self.status = status

    def participant_count(self):
        return Participant.query.filter_by(event=self.id).count

class Participant(db.Model):
    __tablename__ = "participants"
    id = db.Column('participant_id', db.Integer , primary_key=True)
    event = db.Column('event_id', db.Integer, nullable=False)
    fname = db.Column('fname', db.String())
    lname = db.Column('lname', db.String())
    email = db.Column('email', db.String())
    contact = db.Column('contact', db.String())

    def __init__(self, event, fname, lname, email, contact):
        self.id = id
        self.event = event
        self.fname = fname
        self.lname = lname
        self.email = email
        self.contact = contact

