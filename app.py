import flask, time, secrets, os
from PIL import Image
from flask import request, flash, url_for, redirect, render_template
from forms import Registration, LogIn, AddVenue, AddEvent, EventReg, UpdateUser
from flask_login import login_user , logout_user , current_user , login_required, LoginManager
from config import app, db
from Models import Acc, User, Venue, Events, College, Admin_acc
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

@app.route("/")

@app.route("/index", methods=['GET','POST'])
def login():
    form = LogIn(request.form)
    if form.validate_on_submit():
        #Does email exist in db?
        user = Acc.query.filter_by(email=form.email.data).first()
        if user:
            #Is pass correct?
            if user.password == form.password.data:
                #If email exists and pass is correct, login.
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('landing'))
        flash ('Invalid email or password.', 'error')
    return render_template('index.html', form=form)

@app.route("/landing")
@login_required
def landing():
    return render_template('landing.html')

@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    # user = User.query.filter_by(id=id).first()
    # acc = Acc.query.filter_by(id=id).first()
    image_file = url_for('static', filename='images/upload/' + current_user.image_file)
    events = Events.query.all()
    return render_template('profile.html', events=events, image_file=image_file)

@app.route("/settings", methods=['GET','POST'])
@login_required
def editprofile():
    user = User.query.filter_by(id=id).first()
    acc = Acc.query.filter_by(id=id).first()
    form = UpdateUser()
    if form.validate_on_submit():
        user.fname = form.fname.data
        user.lname = form.lname.data
        acc.username = form.username.data
        acc.email = form.email.data
        user.contact = form.contact.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.fname.data = user.fname
        form.lname.data = user.lname
        form.username.data = acc.username
        form.email.data = acc.email
        form.contact.data = user.contact
    image_file = url_for('static', filename='images/upload/' + current_user.image_file)
    return render_template('editprofile.html', image_file=image_file)

@app.route("/logout")
@login_required
def logout():
    flash('You have logged out!')
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET','POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        print form.username.data
        #if username/email is already used
        if Acc.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Try a different username.')
            return redirect(url_for('register'))
        if Acc.query.filter_by(email=form.email.data).first():
            flash('Email already used. Use a different email address.')
            return redirect(url_for('register'))
        #if user,email does not exist yet, and passwords match, register.
        newacc = Acc(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(newacc)
        db.session.commit()
        #user is an account. so create account first before assigning user.
        user = User(Acc.get_id(newacc),form.fname.data, form.lname.data, '')
        db.session.add(user)
        db.session.commit()
        flash('Account created for Acc.username!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login2():
    form = LogIn(request.form)
    if form.validate_on_submit():
        #Does email exist in db?
        user = Acc.query.filter_by(email=form.email.data).first()
        if user:
            #Is pass correct?
            if user.password == form.password.data:
                #If email exists and pass is correct, login.
                login_user(user)
                flash('Logged in successfully.')
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

@app.route("/venue", methods=['GET'])
@login_required
def dispvenue():
    venues = Venue.query.all()
    colleges = College.query.all()
    return render_template('dispvenue.html', venues=venues, colleges=colleges)

@app.route("/venue-main", methods=['GET'])
@login_required
def mainvenue():
    venues = Venue.query.all()
    colleges = College.query.all()
    return render_template('venuemain.html', venues=venues, colleges=colleges)

@app.route("/addvenue", methods=['GET', 'POST'])
@login_required
def addvenue():
    image_file = url_for('static', filename='images/upload/' + Venue.image_file)
    form = AddVenue()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
        #Venues are now all stored in the venues table. They only differ with college id. reference the initialize college script for college ids.
        newvenue = Venue(name=form.name.data, college=form.college.data, capacity=form.capacity.data, rate=form.rate.data, equipment=form.equipment.data, image_file=picture_file)
        #Note that college will accept String values, specifically only those specified in the dictionary added in Models.py
        #If string doesn't match, by default, it will take on the value of 1/ 'MSU-IIT'.
        #Those string values are converted to corresponding id numbers of those colleges in the db.
        db.session.add(newvenue)
        db.session.commit()
        flash('Venue created.')
        return redirect(url_for('venue'))
    return render_template('addvenue.html', form=form, image_file=image_file)

@app.route("/editvenue/<int:id>", methods=['GET', 'POST'])
@login_required
def editvenue(id):
    venue = Venue.query.filter_by(id=id).first()
    image_file = url_for('static', filename='images/upload/' + Venue.image_file)
    form = AddVenue()
    if form.validate_on_submit():
        venue.name = form.name.data
        venue.college = COLLEGENAMES.get(form.college.data)
        venue.capacity = form.capacity.data
        venue.rate = form.rate.data
        venue.equipment = form.equipment.data
        db.session.commit()
        flash('Venue created.')
        return redirect(url_for('venue'))
    return render_template('editvenue.html', form=form, venue=venue, image_file=image_file)

@app.route("/deletevenue/<int:id>", methods=['GET','POST'])
@login_required
def deletevenue(id):
    venue = Venue.query.filter_by(id=id).first()
    if venue != None:
        db.session.delete(venue)
        db.session.commit()
        flash('Event has been deleted.')
    else:
        flash('No such event exists!')
    return redirect(url_for('venue'))

#///////////////////////////// EVENT



@app.route("/addevent", methods=['GET', 'POST'])
@login_required
def addevent():
    image_file = url_for('static', filename='images/upload/' + Venue.image_file)
    form = AddEvent()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
        newevent = Events(organizer=current_user.id, title=form.title.data, description=form.description.data, venue=form.venue.data, tags=form.tags.data, partnum=form.partnum.data, date_s=form.date_s.data, date_e=form.date_e.data, start=form.start.data, end=form.end.data, status='Pending', comment='No Comment', image_file=picture_file)
        db.session.add(newevent)
        db.session.commit()
        flash('Event created. An administrator will approve it later.')
        return redirect(url_for('profile'))
    return render_template('book.html', form=form, image_file=image_file)

disps = [ 
        { 'month':'Jan', 'color':'#781c2e', 'id':'January'},
        { 'month':'Feb', 'color':'#9966cc', 'id':'February'},
        { 'month':'March', 'color':'#7fffd4', 'id':'March'},
        { 'month':'April', 'color':'#cbe3f0', 'id':'April'},
        { 'month':'May', 'color':'#50c878', 'id':'May'},
        { 'month':'June', 'color':'#eae0c8', 'id':'June'},
        { 'month':'July', 'color':'#e0115f', 'id':'July'},
        { 'month':'Aug', 'color':'#e6e200', 'id':'August'},
        { 'month':'Sept', 'color':'#0f52ba', 'id':'September'},
        { 'month':'Oct', 'color':'#b297a0', 'id':'October'},
        { 'month':'Nov', 'color':'#ffc87c', 'id':'November'},
        { 'month':'Dec', 'color':'#40e0d0', 'id':'December'},

]

@app.route("/event/manage", methods=['GET'])
@login_required
def event():
    form = EventReg()
    venues = Venue.query.all()
    events = Events.query.filter_by(status='Pending')
    users = User.query.all()
    return render_template('events.html', form=form, venues=venues, events=events, users=users)

@app.route("/event", methods=['GET'])
def dispevent():
    venues = Venue.query.all()
    events = Events.query.filter_by(status='Pending')
    users = User.query.all()
    return render_template('dispevent.html', venues=venues, events=events, users=users, disps=disps)

@app.route("/editevent/<int:id>", methods=['GET','POST'])
@login_required
def editevent(id):
    event = Events.query.filter_by(id=id).first()
    venue = Venue.query.all()
    image_file = url_for('static', filename='images/upload/' + Event.image_file)
    form = AddVenue() #EditVenue()

    if form.validate_on_submit():
        event.organizer = current_user.id
        event.name = form.name.data
        event.date=form.date.data
        event.time=form.time.data
        event.tags=form.tags.data
        event.venue=form.venue.data
        event.participantnum=form.participantnum.data
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('editevent.html', form=form, event=event, venue=venue, image_file=image_file)

@app.route("/deleteevent/<int:id>", methods=['GET','POST'])
@login_required
def deleteevent(id):
    event = Event.query.filter_by(id=id).first()
    if event != None:
        db.session.delete(event)
        db.session.commit()
        flash('Event has been deleted.')
    else:
        flash('No such event exists!')
    return redirect(url_for('events'))

@app.route("/event/<int:id>/approved", methods=['GET', 'POST'])
@login_required
def approveevent(id):
    event = Events.query.filter_by(id=id).first()
    event.status = 'Approved'
    db.session.commit()
    return redirect(url_for('profile'))

@app.route("/event/<int:id>/rejected", methods=['POST'])
@login_required
def rejectedevent(id):
    event = Events.query.filter_by(id=id).first()
    event.status = 'Rejected'
    db.session.commit()
    return redirect(url_for('profile'))    

@login_manager.user_loader
def load_user(acc_id):
    reg_user = Acc.query.filter_by(id=acc_id).first()
    return reg_user

# db.create_all()
if __name__ == "__main__":
    app.run(debug=True)

