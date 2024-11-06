import traceback
from flask import jsonify, request
from scrapping.Celeb import CelebScrapper
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
        
        if type == SearchItemType.CELEB.value:
            celeb_scrapper = CelebScrapper(id, type)
            scrapped_data = celeb_scrapper.init_scrapping()

            return APIUtils.generate_response(data=scrapped_data)
        elif type == SearchItemType.MOVIE.value:
            return APIUtils.generate_response(error="Not implemented", status_code=501)

        return APIUtils.generate_response(error="Invalid type", status_code=400)
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})