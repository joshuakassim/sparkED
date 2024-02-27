from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Initialize database
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
# Configure session to use filesystem
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# Configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sparkED.db'
# Initialize the app with the extension
db.init_app(app)