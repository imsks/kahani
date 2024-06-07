from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database.models import celeb

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kahani.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized")

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)