import traceback
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database.models import celeb
from utils.api import APIUtils

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kahani.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize the database
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized")

@app.route('/search', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        query = data['query']

        from scrappers.index import Search
        scrapped_data = Search(query)

        return APIUtils.generate_response(data=scrapped_data.get_query_suggestions())
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)