from flask import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# Init DB
@app.cli.command('initdb')
def init_db():
    db.create_all()
