import traceback
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from database.models import db
from routes.scrape import scrape_routes
from routes.search import SearchRoutes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kahani.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/search', methods=['GET'])
def search():
    try:
        search_routes = SearchRoutes()

        if request.method == 'GET':
            query = request.args.get('q')
            return search_routes.search_via_imdb(query)
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})
    
app.route('/scrape', methods=['POST'])(scrape_routes)

# Initialize the database
def init_db():
    with app.app_context():
        migrate.init_app(app, db)
        print("Database initialized")
