import traceback
from flask import jsonify, request
from controllers.scrape import ScrapeController
from utils.api import APIUtils
from utils.contants import SearchItemType

def scrape():
    try:
        data = request.get_json()
        id = data.get('id')
        type = data.get('type')

        if not id:
            return APIUtils.generate_response(error="ID is required", status_code=400)
        if not type:
            return APIUtils.generate_response(error="Type is required", status_code=400)
        
        # Check if type is either celeb, movie or tv show
        if type in [SearchItemType.CELEB.value, SearchItemType.MOVIE.value, SearchItemType.TV_SHOW.value]:
            scrapper = ScrapeController(id, type)
            scrapped_data = scrapper.main() 

            return APIUtils.generate_response(data=scrapped_data)
        else:
            return APIUtils.generate_response(error="Invalid type", status_code=400)
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})
    