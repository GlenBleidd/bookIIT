
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
    3: 'CSM',
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
    profession = db.Column('profession', db.String())
    contact = db.Column('contact', db.String())
    about = db.Column('about', db.String())
    image_file = db.Column('img', db.String(), nullable=False, default='default.png')

    def __init__(self, username, password, email, fname, lname, profession, contact, about):
        self.username = username
        self.type = 0;
        self.password = password
        self.email = email
        self.fname = fname
        self.lname = lname
        self.profession = profession
        self.contact = contact
        self.about = about

    def is_authenticated(self):
        return True

    def is_admin(self):
        return self.type == 1

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
    college = db.Column('admin_college', db.Integer)

    def __init__(self, id, faculty_id, college, contact):
        self.id = id
        self.faculty_id = faculty_id
        self.college = COLLEGENAMES.get(college)

def default_admins():  #makes default admins.
    for x in COLLEGEID:
        test1 = User.query.filter_by(username=COLLEGEID[x]+'_Admin').first()    #test if the college admin account exists.
        if test1 == None:   #if the college admin account does not exist(either because it didn't or it was deleted), then create new account.
            admin = User(username=COLLEGEID[x]+'_Admin',password='1234567890', email='contact@my.iit', fname=COLLEGEID[x], lname='Administrator')
            admin.type = 1
            db.session.add(admin)
            db.session.commit()
            getid = User.query.filter_by(username=COLLEGEID[x]+'_Admin').first().id
            admindetails = Admin_acc(id=getid, faculty_id=x, college=x, contact='+639123456789')
            db.session.add(admindetails)
            db.session.commit()
        else:         #if it exists but is edited, make it into default values
            print test1.id
            test2 = Admin_acc.query.filter_by(id=test1.id).first()                          #get also admin acc details
            test1.username=username=COLLEGEID[x]+'_Admin'
            test1.password='1234567890'
            test1.email='contact@my.iit'
            test1.fname=COLLEGEID[x]
            test1.lname='Administrator'
            if test2 != None:
                test2.faculty_id=x
                test2.college=x
                test2.contact='+639123456789'
            else:
                admindetails = Admin_acc(id=test1.id, faculty_id=x, college=x, contact='+639123456789')
                db.session.add(admindetails)
            db.session.commit()

class Venue(db.Model):
    __tablename__ = "venue"
    id = db.Column('venue_id', db.Integer , primary_key=True)
    college = db.Column('college_id', db.Integer , primary_key=True)
    name = db.Column('venue_name', db.String())
    capacity = db.Column('capacity', db.Integer())
    rate = db.Column('rate', db.Integer)
    equipment = db.Column('equipment', db.String())
    image_file = db.Column('venue_img', db.String(), nullable=False, default='defaultvenue.jp   g')

    def __init__(self, name, college, capacity, rate, equipment, image_file):
        self.name = name
        self.college = college
        self.capacity = capacity
        self.rate = rate
        self.equipment = equipment
        self.image_file = image_file

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '{} - {}'.format(COLLEGEID.get(self.college), self.name)

class College(db.Model):
    __tablename__ = "college"
    id = db.Column('college_id', db.Integer , primary_key=True)
    name = db.Column('college_name', db.String())
    abb = db.Column('college_abb', db.String())
    img = db.Column('college_img', db.String(), nullable=False)

    def __init__(self, name, abb, img):
        self.name = name
        self.abb = abb
        self.img = img

def init_colleges():
    is_existing = College.query.filter_by(id=1).first()
    if is_existing == None:
        newcollege = College(name='MSU-IIT', abb='MSU-IIT', img='IIT.jpg')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='MSU-IIT'
        is_existing.abb='MSU-IIT'
        is_existing.img='IIT.jpg'
        db.session.commit()

    is_existing = College.query.filter_by(id=2).first()
    if is_existing == None:
        newcollege = College(name='College of Engineering', abb='COE', img='COET.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Engineering'
        is_existing.abb='COE'
        is_existing.img='COET.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=3).first()
    if is_existing == None:
        newcollege = College(name='College of Science and Mathematics', abb='CSM', img='CSM.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Science and Mathematics'
        is_existing.abb='CSM'
        is_existing.img='CSM.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=4).first()
    if is_existing == None:
        newcollege = College(name='College of Education', abb='CED', img='CED.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Education'
        is_existing.abb='CED'
        is_existing.img='CED.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=5).first()
    if is_existing == None:
        newcollege = College(name='College of Arts and Social Science', abb='CASS', img='CASS.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Arts and Social Science'
        is_existing.abb='CASS'
        is_existing.img='CASS.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=6).first()
    if is_existing == None:
        newcollege = College(name='College of Business Administration and Accountancy', abb='CBAA', img='CBAA.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Business Administration and Accountancy'
        is_existing.abb='CBAA'
        is_existing.img='CBAA.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=7).first()
    if is_existing == None:
        newcollege = College(name='College of Nursing', abb='CON', img='nursing.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Nursing'
        is_existing.abb='CON'
        is_existing.img='nursing.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=8).first()
    if is_existing == None:
        newcollege = College(name='School of Computer Studies', abb='SCS', img='SCS.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='School of Computer Studies'
        is_existing.abb='SCS'
        is_existing.img='SCS.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=9).first()
    if is_existing == None:
        newcollege = College(name='Integrated Developmental School', abb='IDS', img='IDS.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='Integrated Developmental School'
        is_existing.abb='IDS'
        is_existing.img='IDS.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=10).first()
    if is_existing == None:
        newcollege = College(name='PRISM', abb='PRISM', img='PRISM.jpg')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='PRISM'
        is_existing.abb='PRISM'
        is_existing.img='PRISM.jpg'
        db.session.commit()

class Events(db.Model):
    __tablename__ = "events"
    organizer = db.Column('organizer_id', db.Integer)
    venue = db.Column('venue_id', db.Integer)
    id = db.Column('event_id', db.Integer , primary_key=True)
    title = db.Column('event_name', db.String())
    description = db.Column('event_desc', db.String())
    tags = db.Column('event_tags', db.String())
    date_s = db.Column('event_date_start', db.Date())
    start = db.Column('event_time_start', db.Time())
    date_e = db.Column('event_date_end', db.Date())
    end = db.Column('event_time_end', db.Time())
    status = db.Column('event_status', db.String())
    comment = db.Column('event_comment', db.String())
    requestdate = db.Column('event_request_date', db.Date())
    image_file = db.Column('event_img', db.String(), nullable=False, default='defaultevents.jpg')

    def __init__(self, organizer, venue, title, description, tags, date_s, start, date_e, end, status, comment, image_file, requestdate):
        self.organizer = organizer
        self.title = title
        self.description = description
        self.venue = venue
        self.tags = tags
        self.start = start
        self.end = end
        self.date_s =date_s
        self.date_e = date_e
        self.status = status
        self.comment = comment
        self.image_file = image_file
        self.requestdate = requestdate

    def participant_count(self):
        return Participant.query.filter_by(event=self.id).count

class Participant(db.Model):
    __tablename__ = "participants"
    id = db.Column('particpant_id', db.Integer , primary_key=True)
    event = db.Column('event_id', db.Integer, nullable=False)
    fname = db.Column('fname', db.String())
    lname = db.Column('lname', db.String())
    email = db.Column('email', db.String())
    contact = db.Column('contact', db.String())

    def __init__(self, event, fname, lname, email, contact):
        self.event = event
        self.fname = fname
        self.lname = lname
        self.email = email
        self.contact = contact

