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
        elif not type:
            return APIUtils.generate_response(error="Type is required", status_code=400)
        elif type not in [SearchItemType.CELEB.value, SearchItemType.MOVIE.value, SearchItemType.TV_SHOW.value]:
            return APIUtils.generate_response(error="Invalid type", status_code=400)
        
        scrapper = ScrapeController(id, type)
        scrapped_data = scrapper.main() 

        return APIUtils.generate_response(data=scrapped_data)
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})
    