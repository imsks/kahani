import traceback
from flask import jsonify, request
from controllers.scrape import Scrape
from database.models import Movie
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

        # 1. Store the scrapped data in the database
        # Store Data in Movies
        celeb_id = scrapped_data.get('celeb_id')
        celeb_filmography = scrapped_data.get('celeb_filmography')

        for film in celeb_filmography['actor']:
            # Store Films and Movie + Celeb + Role
            Movie().store_movie(film)

        # 2. Return the scrapped data

        return APIUtils.generate_response(data=scrapped_data)
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})