import traceback
from flask import jsonify, request
from controllers.search import Search
from database.models import Celeb, Movie
from utils.api import APIUtils
from utils.contants import SearchItemType

class SearchRoutes:
# Search From API
    def search_via_imdb(self, query):
        try:
            if not query:
                return APIUtils.generate_response(error="Query is required", status_code=400)

            searched_data = Search(query).get_query_suggestions()

            for item in searched_data:
                if item["type"] == SearchItemType.CELEB.value:
                    Celeb().store_celeb(item)
                else:
                    Movie().store_movie(item)

            return APIUtils.generate_response(data=searched_data)
        except Exception as e:
            print(traceback.print_exc())
            return jsonify({"error": str(e)})