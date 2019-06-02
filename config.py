from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testfile'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:regards@localhost:5432/BookIT'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/BookIT'

app.static_folder = 'static'

db = SQLAlchemy(app)