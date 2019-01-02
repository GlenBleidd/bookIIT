from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, InputRequired
from wtforms_components import TimeField 
import config


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

#def validate_username(self, username):
	#user = User.query.filter_by(username=username.data).first()
	#if user:
		#raise ValidationError('That username already exists! Please use a different one.')

#def validate_email(self, email):
	#user = User.query.filter_by(email=email.data).first()
	#if user:
		#raise ValidationError('That e-mail is already in use! Please use a different one.')

class UpdateUser(FlaskForm):
	fname = StringField('First Name',
							validators=[InputRequired(), Length(min=2, max=20)])
	lname = StringField('Last Name',
							validators=[InputRequired(), Length(min=2, max=20)])
	username = StringField('Username',
							validators=[InputRequired(), Length(min=5, max=16)])
	email = StringField('Email',
							validators=[InputRequired(), Email()])
	contact = IntegerField('Contact', 
							validators=[Optional()])
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
	description = StringField('Description',
							validators=[DataRequired()])
	venue = SelectField('Venue',
							validators=[DataRequired()], choices=[('1', 'Gymnasium'), ('3','ICT 3H'), ('4', 'HUBPORT')])
	tags = StringField('Tags',
							validators=[Optional()])
	partnum = IntegerField('Participants',
							validators=[Optional()])
	date_s = DateField('Date', 
							validators=[DataRequired()])
	date_e = DateField('Date', 
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