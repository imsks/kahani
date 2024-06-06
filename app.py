from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database.models import celeb, movie, role, genre, movie_celeb_role

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kahani.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Init DB
@app.cli.command('initdb')
def init_db():
    db.create_all()
