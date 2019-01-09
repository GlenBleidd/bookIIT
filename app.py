import flask, time, secrets, os
from PIL import Image
from flask import request, flash, url_for, redirect, render_template
from forms import Registration, LogIn, AddVenue, AddEvent, EventReg, UpdateUser, Participate, Results
from flask_login import login_user , logout_user , current_user , login_required, LoginManager
from config import app, db
from Models import *
import datetime
from datetime import timedelta
from time import gmtime, strftime

strftime("%Y-%m-%d %H:%M:%S", gmtime())

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "You have logged out."

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/upload', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

#//////////////////////////USER COMMON ROUTES
@app.route("/")

@app.route("/index", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/landing')
    else:
        form = LogIn(request.form)
        if form.validate_on_submit():
            #Does email exist in db?
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                #Is pass correct?
                if user.password == form.password.data:
                    #If email exists and pass is correct, login.
                    login_user(user)
                    flash('Logged in successfully.', 'login')
                    return redirect(url_for('landing'))
            flash ('Invalid email or password.', 'error')
        return render_template('index.html', form=form)

@app.route("/landing")
@login_required
def landing():
    if current_user.is_admin():
        return render_template('landing.html')
    else:
        return redirect('/profile')

@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    form = UpdateUser()
    accs = Admin_acc.query.all()
    colleges = College.query.all()
    participants = Participant.query.all()
    users = User.query.filter_by(type=0)
    admins = User.query.filter_by(type=1)
    image_file = url_for('static', filename='images/upload/' + current_user.image_file)
    events = Events.query.all()
    return render_template('profile.html', participants=participants, accs=accs, colleges=colleges, events=events, users=users, admins=admins, form=form, image_file=image_file)

@app.route("/settings", methods=['GET','POST'])
@login_required
def editprofile():
    user = User.query.filter_by(id=current_user.id).first()
    form = UpdateUser()
    if form.validate_on_submit():
        #if username/email is already used
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose another.','error')
            return redirect(url_for('editprofile'))
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists. Please choose another.','error')
            return redirect(url_for('editprofile'))
        else:
            user.fname = form.fname.data
            user.lname = form.lname.data
            user.username = form.username.data
            user.email = form.email.data
            user.contact = form.contact.data
            db.session.commit()
            flash('Your account has been updated!','success')
            return redirect(url_for('profile'))
    image_file = url_for('static', filename='images/upload/' + current_user.image_file)
    return render_template('editprofile.html', image_file=image_file, form=form, user=user)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Organizer': #if Searching for Organizer name(works with either searching first or last name)
            qry = db.query(Events, User).filter(User.id==Events.organizer).filter(User.fname.contains(search_string))
            qry2 = db.query(Events, User).filter(User.id==Events.organizer).filter(User.lname.contains(search_string))
            qry3= qry.union(qry2)
            results = [item[0] for item in qry3.all()]
        elif search.data['select'] == 'Event Title':
            qry = db.query(Events).filter(Events.title.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Event Tags':
            qry = db.query(Events).filter(Events.tags.contains(search_string))
            results = qry.all()
        else:
            qry = db.query(Events)
            results = qry.all()

        if not results:
            flash('No results found!', 'search')
            return redirect(url_for('profile'))
        else:
            table = Results(results)
            table.border = True
            return render_template('results.html', table=table)

@app.route("/logout")
@login_required
def logout():
    flash('You have logged out!','logout')
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/landing')
    else:
        form = Registration()
        if form.validate_on_submit():
            #if username/email is already used
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists. Try a different username.','error')
                return redirect(url_for('register'))
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already used. Use a different email address.','error')
                return redirect(url_for('register'))
            #if user,email does not exist yet, and passwords match, register.
            newacc = User(username=form.username.data, password=form.password.data, email=form.email.data, fname=form.fname.data, lname=form.lname.data)
            db.session.add(newacc)
            db.session.commit()
            flash('Account has been created! You have now logged in!','success')
            getuser = User.query.filter_by(username=newacc.username).first()
            login_user(getuser)
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login2():
    if current_user.is_authenticated:
        return redirect('/landing')
    else:
        form = LogIn(request.form)
        if form.validate_on_submit():
            #Does email exist in db?
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                #Is pass correct?
                if user.password == form.password.data:
                    #If email exists and pass is correct, login.
                    login_user(user)
                    flash('Logged in successfully.','login')
                    return redirect(url_for('landing'))
            flash ('Invalid email or password.', 'error')
        return render_template('login.html', form=form)

#//////////////////////////VENUES
@app.route("/venue/manage", methods=['GET'])
@login_required
def venue():
    venues = Venue.query.all()
    colleges = College.query.all()
    return render_template('venue.html', venues=venues, colleges=colleges)

@app.route("/venue/<int:id>", methods=['GET'])
@login_required
def dispvenue(id):
    venues = Venue.query.filter_by(college=id)
    colleges = College.query.all()
    admins = Admin_acc.query.filter_by(college=id)
    users = User.query.filter_by(type=1)
    return render_template('dispvenue.html', venues=venues, admins=admins, users=users, colleges=colleges)

@app.route("/venue-main", methods=['GET'])
@login_required
def mainvenue():
    venues = Venue.query.all()
    colleges = College.query.all()
    return render_template('venuemain.html', venues=venues, colleges=colleges)

@app.route("/addvenue", methods=['GET', 'POST'])
@login_required
def addvenue():
    if not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('profile'))
    else:
        image_file = url_for('static', filename='images/upload/' + Venue.image_file)
        form = AddVenue()
        if form.validate_on_submit():
            if form.image_file.data:
                picture_file = save_picture(form.image_file.data)
            newvenue = Venue(name=form.name.data, college=form.college.data, capacity=form.capacity.data, rate=form.rate.data, equipment=form.equipment.data, image_file=picture_file)
            db.session.add(newvenue)
            db.session.commit()
            flash('Venue created.','success')
            return redirect(url_for('venue'))
        return render_template('addvenue.html', form=form, image_file=image_file)

@app.route("/editvenue/<int:id>", methods=['GET', 'POST'])
@login_required
def editvenue(id):
    if not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('profile'))
    else:
        venue = Venue.query.filter_by(id=id).first()
        image_file = url_for('static', filename='images/upload/' + Venue.image_file)
        form = AddVenue()
        if form.validate_on_submit():
            if form.image_file.data: #if change in picture, replace picture. otherwise, stay the same
                picture_file = save_picture(form.image_file.data)
                venue.image_file = picture_file
            venue.name = form.name.data
            venue.college = form.college.data
            venue.capacity = form.capacity.data
            venue.rate = form.rate.data
            venue.equipment = form.equipment.data
            db.session.commit()
            flash('Venue created.','success')
            return redirect(url_for('venue'))
        return render_template('editvenue.html', form=form, venue=venue, image_file=image_file)

@app.route("/deletevenue/<int:id>", methods=['GET','POST'])
@login_required
def deletevenue(id):
    if not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('profile'))
    else:
        venue = Venue.query.filter_by(id=id).first()
        events = Events.query.filter_by(venue=venue.id)
        if venue != None:
            for event in events:
                flash('NOTICE: An event has been removed because the venue of the event has become unavailable.','Notify'+str(event.organizer))
                db.session.delete(event)
                db.session.commit()
            db.session.delete(venue)
            db.session.commit()
            flash('Event has been deleted.','success')
        else:
            flash('No such event exists!')
        return redirect(url_for('venue'))

#///////////////////////////// EVENT
def check_availability(date_s, date_e, start, end, venue): #returns true if available
    events = Events.query.filter_by(venue=venue) #list all events in a venue
    res = False
    for event in events:
        if event.status == 'Approved':
            if event.date_s == event.date_e and event.date_s == date_s and date_e == 'None':#if event is 1 day, check if any overlapping times.
                overlap = start < event.end and event.start < end
            else:
                overlap = date_s < event.date_e and event.date_s < date_e #if more than 1 day event, check if days intersect
            res = res or overlap
    return not res

@app.route("/addevent", methods=['GET', 'POST'])
@login_required
def addevent():
    image_file = url_for('static', filename='images/upload/' + Venue.image_file)
    form = AddEvent()
    datetimenow = datetime.date.today()
    weekfromnow = datetime.date.today() - timedelta(days=7)
    if form.validate_on_submit():
        if (form.date_s.data < datetimenow):
            flash('Error. Date or Time start chosen has already passed!','error')
        elif(form.date_s.data < weekfromnow):
            flash('Error. You can only book dates from at least one week from today!','error')
        elif not check_availability(form.date_s.data, form.date_e.data, form.start.data, form.end.data, form.venue.data.id): #if not available
            flash('Venue has been booked for another event at this time.','error')
        else:
            if form.image_file.data:
                picture_file = save_picture(form.image_file.data)
            if form.date_e.data == None:
                newevent = Events(organizer=current_user.id, title=form.title.data, description=form.description.data, venue=form.venue.data.id, tags=form.tags.data, date_s=form.date_s.data,start=form.start.data, date_e=form.date_s.data,end=form.end.data, status='Pending', comment='',image_file=picture_file, requestdate=datetime.datetime.today())
            else:
                newevent = Events(organizer=current_user.id, title=form.title.data, description=form.description.data, venue=form.venue.data.id, tags=form.tags.data, date_s=form.date_s.data,start=form.start.data, date_e=form.date_e.data,end=form.end.data, status='Pending', comment='',image_file=picture_file, requestdate=datetime.datetime.today())
            db.session.add(newevent)
            db.session.commit()
            flash('Event created. An administrator will approve it later.','success')
            return redirect(url_for('profile'))
    return render_template('book.html', form=form, image_file=image_file)

disps = [
        { 'month':'Jan', 'color':'#781c2e', 'id':'January'},
        { 'month':'Feb', 'color':'#9966cc', 'id':'February'},
        { 'month':'March', 'color':'#7fffd4', 'id':'March'},
        { 'month':'April', 'color':'#cbe3f0', 'id':'April'},
        { 'month':'May', 'color':'#50c878', 'id':'May'},
        { 'month':'June', 'color':'#eae0c8', 'id':'June'},
        { 'month':'July', 'color':'#80461b', 'id':'July'},
        { 'month':'Aug', 'color':'#e6e200', 'id':'August'},
        { 'month':'Sept', 'color':'#0f52ba', 'id':'September'},
        { 'month':'Oct', 'color':'#b297a0', 'id':'October'},
        { 'month':'Nov', 'color':'#ffc87c', 'id':'November'},
        { 'month':'Dec', 'color':'#40e0d0', 'id':'December'},

]

def Autorejecter():
    events = Events.query.all()
    for event in events:
        if(event.status == 'Pending' and event.requestdate < datetime.date.today()):
            event.status = 'Rejected.'
            event.comment = 'Time has already lapsed. Please Rebook or Cancel this request.'
            db.session.commit()

@app.route("/event/manage", methods=['GET'])
@login_required
def event():
    if not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('profile'))
    else:
        form = EventReg()
        venues = Venue.query.all()
        # events = Events.query.filter_by(status='Pending')
        events = Events.query.all()
        users = User.query.all()
        return render_template('events.html', form=form, venues=venues, events=events, users=users)

@app.route("/event", methods=['GET', 'POST'])
def dispevent():
    venues = Venue.query.all()
    form = Participate()
    Autorejecter()
    participants = Participant.query.all()
    events = Events.query.filter_by(status='Approved')
    users = User.query.all()
    if form.validate_on_submit():
        newparticipant = Participant(event=form.eventid.data, fname=form.fname.data, lname=form.lname.data, email=form.email.data, contact=form.contact.data)
        db.session.add(newparticipant)
        db.session.commit()
        flash('Participant added.','success')
        return redirect('/event')
    return render_template('dispevent.html', participants=participants, venues=venues, events=events, users=users, form=form, disps=disps)

@app.route("/event/<int:id>/participants", methods=['GET'])
def participantlist():
    venues = Venue.query.all()
    events = Events.query.filter_by(status='Approved')
    participants = Participant.query.all()
    return render_template('dispevent.html', venues=venues, events=events, participants=participants)

@app.route("/deleteparticipant/<int:id>", methods=['GET','POST'])
@login_required
def delparticipant(id):
    participant = Participant.query.filter_by(id=id).first()
    event = Events.query.filter_by(id = participant.event).first()
    if current_user.is_admin() or current_user.id == event.organizer:
        db.session.delete(participant)
        db.session.commit()
        return redirect('/event')
    else:
        flash('Error. You have no permission to delete this participant from the event.','error')
        return redirect('/event')

@app.route("/editevent/<int:id>", methods=['GET','POST'])
@login_required
def editevent(id):
    event = Events.query.filter_by(id=id).first()
    venue = Venue.query.all()
    image_file = url_for('static', filename='images/upload/' + Events.image_file)
    form = AddEvent() #EditVenue()
    datetimenow = datetime.date.today()
    weekfromnow = datetime.date.today() - timedelta(days=7)
    if form.validate_on_submit():
        if (form.date_s.data < datetimenow):
            flash('Error. Date or Time start chosen has already passed!','error')
        elif(form.date_s.data < weekfromnow):
            flash('Error. You can only book dates from at least one week from today!','error')
        elif not check_availability(form.date_s.data, form.date_e.data, form.start.data, form.end.data, form.venue.data.id, event.id): #if not available
            flash('Venue has been booked for another event at this time.','error')
        else:
            if form.image_file.data: #if replacement image exists, replace image. Otherwise, don't edit.
                picture_file = save_picture(form.image_file.data)
                event.image_file=picture_file
            event.description=form.description.data
            event.name = form.name.data
            event.date_s=form.date_s.data
            event.start=form.start.data
            event.date_e=form.date_e.data
            event.end=form.end.data
            event.tags=form.tags.data
            event.venue=form.venue.data.id
            event.status='Pending'
            event.comment='Venue has changed. Need approval from administrator.'
            event.requestdate=datetime.datetime.today()
            db.session.commit()
            flash('Your event details have been changed.','success')
            return redirect(url_for('profile'))
    return render_template('rebook.html', form=form, event=event, venue=venue, image_file=image_file)

@app.route("/deleteevent/<int:id>", methods=['GET','POST'])
@login_required
def deleteevent(id):
    event = Events.query.filter_by(id=id).first()
    if event != None:
        participantlist = Participant.query.filter_by(event=event.id)
        for p in participantlist:
            db.session.delete(p)    
            db.session.commit()
        db.session.delete(event)
        db.session.commit()
        flash('Event has been deleted.','success')
    else:
        flash('No such event exists!','error')
    return redirect(url_for('profile'))

@app.route("/event/<int:id>/approved", methods=['GET', 'POST'])
@login_required
def approveevent(id):
    if not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('profile'))
    else:
        event = Events.query.filter_by(id=id).first()
        event.status = 'Approved'
        db.session.commit()
        flash('Your event has been approved!','Notify'+str(event.organizer))
        return redirect(url_for('event'))

@app.route("/event/<int:id>/rejected", methods=['POST'])
@login_required
def rejectedevent(id):
    if not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('venue'))
    else:
        event = Events.query.filter_by(id=id).first()
        event.status = 'Rejected'
        db.session.commit()
        flash('Your event has been rejected! Please review it as soon as possible.','Notify'+str(event.organizer))
        return redirect(url_for('profile'))

@app.route("/event/<int:id>/participants", methods=['GET','POST'])
@login_required
def participant_list(id):
    event = Events.query.filter_by(id=id).first()
    if current_user.id != event.organizer or not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('events'))
    else:
        participants = Participant.query.filter_by(event=id)
        return render_template('events.html') #return render_template('participant_list.html', event=event, participants=participants)

@app.route("/event/<int:id>/invite", methods=['GET','POST'])
@login_required
def invite(id):
    form = Participate()
    event = Events.query.filter_by(id=id).first()
    if event.status != 'Approved' or event == None:
        flash('No such event booked or approved.','error')
    else:
        newparticipant = Participant(event=id, fname=form.fname.data, lname=form.lname.data, email=form.email.data, contact=form.contact.data)
        db.session.add(newparticipant)
        db.session.commit()
        flash('Person invited to event.','success')
        return redirect(url_for('profile'))
    return render_template('profile.html') #return render_template('invite.html', event=event)

@app.route("/event/<int:id>/participate", methods=['GET','POST'])
def participate(id):
    form = Participate()
    event = Events.query.filter_by(id=id).first()
    if event.status != 'Approved' or event == None:
        flash('No such event booked or approved.','error')
    else:
        newparticipant = Participant(event=id, fname=form.fname.data, lname=form.lname.data, email=form.email.data, contact=form.contact.data)
        db.session.add(newparticipant)
        db.session.commit()
        flash('Participant added.','success')
        return redirect(url_for('profile'))
    if current_user != None:
        return render_template('profile.html') #return render_template('participate.html', event=event, user=current_user)
    else:
        return render_template('profile.html') #return render_template('participate.html', event=event)

#//////////////////////////ADMIN STUFF: EDIT ADMIN PROFILE
def init_admin_details(id):
    admin_details = Admin_acc.query.filter_by(id=id).first()
    if admin_details == None: #if admin details doesnt exist, initialize. if it does, do nothing
        user = User.query.filter_by(id=id).first()
        new_admin = Admin_acc(id=id, faculty_id='Tempidfor_'+user.username, college=0, contact='+639123456789')
        db.session.add(new_admin)
        db.session.commit()

@app.route("/settings-admin", methods=['GET','POST'])
@login_required
def editadmin():
    user = User.query.filter_by(id=current_user.id).first()
    init_admin_details(id=current_user.id)
    admindetails = Admin_acc.query.filter_by(id=current_user.id).first()
    form = UpdateUser()
    if form.validate_on_submit():
        #if username/email is already used
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose another.','error')
            return redirect(url_for('editprofile'))
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists. Please choose another.','error')
            return redirect(url_for('editprofile'))
        else:
            user.fname = form.fname.data
            user.lname = form.lname.data
            user.username = form.username.data
            user.email = form.email.data
            user.contact = form.contact.data
            db.session.commit()
            flash('Your account has been updated!','success')
            return redirect(url_for('profile'))
    image_file = url_for('static', filename='images/upload/' + current_user.image_file)
    return render_template('editprofile.html', image_file=image_file, form=form, user=user)

#(self, id, faculty_id, college, contact):
#//////////////////////////ADMIN STUFF: MANAGE USERS

@app.route("/manageusers", methods=['GET','POST'])
@login_required
def manageusers():
    if not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('profile'))
    else:
        userlist = User.query.filter_by(type=0) #this is a user list of Non-Admin Users
        return render_template('manageusers.html', userlist=userlist)

@app.route("/user/<int:id>/edit", methods=['GET','POST'])
@login_required
def edituser():
    if not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('profile'))
    else:
        user = User.query.filter_by(id=id).first()
        form = UpdateUser()
        if form.validate_on_submit():
            #if username/email is already used
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists. Please choose another.','error')
                return redirect(url_for('editprofile'))
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already exists. Please choose another.','error')
                return redirect(url_for('editprofile'))
            else:
                user.fname = form.fname.data
                user.lname = form.lname.data
                user.username = form.username.data
                user.email = form.email.data
                user.contact = form.contact.data
                db.session.commit()
                flash('Your account has been updated!','success')
                return redirect(url_for('profile'))
    image_file = url_for('static', filename='images/upload/' + current_user.image_file)
    return render_template('editprofile.html', image_file=image_file, form=form, user=user)

@app.route("/user/<int:id>/delete", methods=['GET','POST'])
@login_required
def deleteuser():
    if not current_user.is_admin():
        flash("You don't have permission to access this page.",'error')
        return redirect(url_for('profile'))
    else:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        flash('User has been deleted!','success')
        return redirect(url_for('usermanage'))

#//////////////////////////SV_CHEATS 1
#The debugging routes.

@app.route("/toggleadmin") #toggles current_user's is_admin status
def adminme():
    user = User.query.filter_by(id=current_user.id).first()
    if user == None:
        return redirect('/login')
    if user.type == 1:
        user.type = 0
    elif user.type == 0:
        user.type = 1
    db.session.commit()
    return redirect('/landing')

@app.route("/makedefaultadmins")#creates all the default admins.
def makeadmins():
    default_admins()
    return redirect('/landing')

@login_manager.user_loader
def load_user(acc_id):
    reg_user = User.query.filter_by(id=acc_id).first()
    return reg_user

# db.create_all()
if __name__ == "__main__":
    app.run(debug=True)

