import traceback
from flask import jsonify, request
from controllers.scrape import Scrape
from database.models import Celeb, Movie, MovieCelebRole, Scrapped
from utils.api import APIUtils
from utils.contants import CelebRoles

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
        # Store Scrapping log
        Scrapped().store_scrapped({
                "id": id,
                "type": type
            })

        # 1. Store the scrapped data in the database
        # Store Data in Movies
        celeb_id = scrapped_data.get('celeb_id')
        celeb_filmography = scrapped_data.get('celeb_filmography')
        
        role_to_enum = {
            'actor': CelebRoles.ACTOR,
            'writer': CelebRoles.WRITER,
            'director': CelebRoles.DIRECTOR,
            'producer': CelebRoles.PRODUCER,
        }

        # Create a list of the keys (roles) to iterate over
        roles = ['actor', 'writer', 'director', 'producer']

        # Loop through each role
        for role in roles:
            # Get the corresponding CelebRoles enum value
            celeb_role_enum = role_to_enum.get(role)

            if celeb_role_enum:
                for movie in celeb_filmography[role]:
                    # Store the movie and its associated role
                    Movie().store_movie(movie)
                    MovieCelebRole().store_movie_celeb_role(movie.get('id'), celeb_id, celeb_role_enum.value)

        # 2. Return the scrapped data
        return APIUtils.generate_response(data=scrapped_data)
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"error": str(e)})