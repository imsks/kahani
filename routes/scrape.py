import traceback
from flask import jsonify, request
from controllers.scrape import ScrapeController
from utils.api import APIUtils
from utils.contants import SearchItemType
from database.models import Scrapped


def scrape():
    try:
        data = request.get_json()
        id = data.get('id')
        type = data.get('type')
        force_scrape = data.get('force_scrape', False)

        errors = {
            not id: "ID is required",
            not type: "Type is required",
            type not in [SearchItemType.CELEB.value, SearchItemType.MOVIE.value, SearchItemType.TV_SHOW.value]: "Invalid type"
        }

        for condition, error_message in errors.items():
            if condition:
                return APIUtils.generate_response(error=error_message, status_code=400)
            
        response = None
        scrapped = Scrapped(id=id, type=type)
            
        # Check if data is already scrapped
        if force_scrape is True or not scrapped.is_scrapped(id, type):
            scrapper = ScrapeController(id, type)
            response = scrapper.main()

        # Fetch All Celeb Data from the database
        else:
            response = scrapped.get_scrapped_data(id, type)

        return APIUtils.generate_response(data=response)
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})
    