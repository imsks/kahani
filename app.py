import traceback
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from controllers.scrape import Scrape
from controllers.search import Search
from database.models.celeb import Celeb
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
def search():
    try:
        data = request.get_json()
        query = data.get('query')

        if not query:
            return APIUtils.generate_response(error="Query is required", status_code=400)

        searched_data = Search(query)

        for item in searched_data:
            if item["type"] == "Celeb":
                Celeb.store_celeb(item)

        return APIUtils.generate_response(data=searched_data.get_query_suggestions())
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})
    
@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        id = data.get('id')
        type = data.get('type')

        if not id:
            return APIUtils.generate_response(error="ID is required", status_code=400)
        if not type:
            return APIUtils.generate_response(error="Type is required", status_code=400)

        scrapped_data = Scrape(id, type).init_scrapping()

        return APIUtils.generate_response(data=scrapped_data)
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)