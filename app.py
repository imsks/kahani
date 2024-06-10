import traceback
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database.models import celeb

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kahani.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize the database
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized")

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        print(data)
        from scrappers import scrape_celeb
        celeb_data = scrape_celeb()
        return jsonify(celeb_data)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)