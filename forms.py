from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField, TextAreaField, DateTimeField
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
							validators=[DataRequired()], choices=[('MSU-IIT', 'MSU-IIT'), ('College of Engineering and Technology', 'College of Engineering and Technology'), ('College of Science and Mathematics', 'College of Science and Mathematics'), ('College of Education', 'College of Education'), ('College of Arts and Social Sciences', 'College of Arts and Social Sciences'), ('College of Business Administration and Accountancy', 'College of Business Administration and Accountancy'), ('College of Nursing', 'College of Nursing'), ('School of Computer Studies', 'School of Computer Studies'), ('Integrated Developmental School', 'Integrated Developmental School'), ('Premier Research Institute of Science and Mathematics', 'Premier Research Institute of Science and Mathematics')])
	capacity = IntegerField('Capacity',
							validators=[Optional()])
	rate = IntegerField('Rate',
							validators=[Optional()])
	equipment = TextAreaField('Equipment',
							validators=[Optional()])
	submit = SubmitField('Add Venue')

class AddEvent(FlaskForm):
	title = StringField('Title',
							validators=[DataRequired()])
	description = StringField('Description',
							validators=[DataRequired()])
	venue = QuerySelectField(query_factory=lambda: Models.Venue.query.all(), allow_blank=False, get_label='name')
	tags = StringField('Tags',
							validators=[Optional()])
	partnum = IntegerField('Participants',
							validators=[Optional()])
	date_s = DateField('Start Date',
						  validators=[DataRequired()])
	start = TimeField('Start Time',
							validators=[DataRequired()])
	date_e = DateField('End Date',
						  validators=[DataRequired()])
	end = TimeField('End Time',
							validators=[DataRequired()],)
	submit = SubmitField('Request Event')
	image_file = FileField('Event Poster', 
							validators=[FileAllowed(['jpg', 'png'])])

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