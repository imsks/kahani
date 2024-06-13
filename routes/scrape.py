import traceback
from flask import jsonify, request
from controllers.scrape import Scrape
from utils.api import APIUtils

def scrape_routes():
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