from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField, TextAreaField, FileField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, InputRequired
from wtforms_components import TimeField
from flask_table import Table, Col
import config, Models

import wtforms_sqlalchemy.fields as f
def get_pk_from_identity(obj):
	cls, key = f.identity_key(instance=obj)[:2]
	return ':'.join(f.text_type(x) for x in key)
f.get_pk_from_identity = get_pk_from_identity

class Registration(FlaskForm):
	fname = StringField('First Name',
							validators=[InputRequired(), Length(min=2, max=20)])
	lname = StringField('Last Name',
							validators=[InputRequired(), Length(min=2, max=20)])
	username = StringField('Username',
							validators=[InputRequired(), Length(min=5, max=16)])
	email = StringField('Email',
							validators=[InputRequired(), Email()])
	password = PasswordField('Password',
							validators=[InputRequired(), EqualTo('confirm_password', message='Passwords do not match,')])
	confirm_password = PasswordField('Confirm Password',
							validators=[InputRequired()])

class UpdateUser(FlaskForm):
	fname = StringField('First Name',
							validators=[InputRequired(), Length(min=2, max=20)])
	lname = StringField('Last Name',
							validators=[InputRequired(), Length(min=2, max=20)])
	username = StringField('Username',
							validators=[InputRequired(), Length(min=5, max=16)])
	email = StringField('Email',
							validators=[InputRequired(), Email()])
	profession = StringField('Profession',
							validators=[Optional()])
	bio = TextAreaField('Bio',
							validators=[Optional()])
	contact = IntegerField('Contact',
							validators=[Optional()])
	image_file = FileField('Update Picture',
							validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose another.')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please choose another.')


class LogIn(FlaskForm):
	email = StringField('Email',
							validators=[InputRequired(), Email()])
	password = PasswordField('Password',
							validators=[InputRequired()])
	remember = BooleanField('Remember Me')

class AddVenue(FlaskForm):
	name = StringField('Venue Name',
							validators=[DataRequired()])
	college = SelectField('College', id='college_id',
							validators=[DataRequired()], choices=[('1', 'MSU-IIT'), ('2', 'College of Engineering and Technology'), ('3', 'College of Science and Mathematics'), ('4', 'College of Education'), ('5', 'College of Arts and Social Sciences'), ('6', 'College of Business Administration and Accountancy'), ('7', 'College of Nursing'), ('8', 'School of Computer Studies'), ('9', 'Integrated Developmental School'), ('10', 'Premier Research Institute of Science and Mathematics')])
	capacity = IntegerField('Capacity',
							validators=[Optional()])
	rate = IntegerField('Rate',
							validators=[Optional()])
	equipment = TextAreaField('Equipment',
							validators=[Optional()])
	image_file = FileField('Update Picture',
							validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Add Venue')


class AddEvent(FlaskForm):
	title = StringField('Title',
							validators=[DataRequired()])
	description = TextAreaField('Description',
							validators=[DataRequired()])
	venue = QuerySelectField(query_factory=lambda: Models.Venue.query.all(), allow_blank=False, get_label='name')
	tags = StringField('Tags',
							validators=[Optional()])
	partnum = IntegerField('Participants',
							validators=[Optional()])
	date_s = DateField('Start Date',
							validators=[DataRequired()])
	date_e = DateField('End Date',
							validators=[Optional()])
	start = TimeField('Start Time',
							validators=[DataRequired()])
	end = TimeField('End Time',
							validators=[DataRequired()])
	image_file = FileField('Event Poster',
							validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Request Event')

class EventReg(FlaskForm):
	regid = StringField('Title',
							validators=[DataRequired()])
	eventid = IntegerField('Event ID',
							validators=[DataRequired()])
	userid = IntegerField('User ID',
							validators=[DataRequired()])
	comment = TextAreaField('Comments/Suggestions',
							validators=[DataRequired()])
	submit = SubmitField('Submit')

class Participate(FlaskForm):
    fname = StringField('First Name',
                        validators=[InputRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name',
                        validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    contact = StringField('Contact Number',
                          validators=[InputRequired(), Length(min=2, max=20)])

class Results(Table):
    id = Col('Id', show= False)
    organizer = Col('Organizer')
    venue = Col('Venue')
    title = Col('Title')
    tags = Col('Tags')
    date_s = Col('Date Start')
    time_s = Col('Time Start')
    date_e = Col('Date End')
    time_e = Col('Time End')