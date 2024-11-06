from controllers.scrape import Scrape
from database.models import Movie, MovieCelebRole, Scrapped
from utils.contants import CelebRoles

class CelebScrapper:
    def __init__(self, id, type):
        self.id = id
        self.type = type
    
    def init_scrapping(self):
        scrapped_data = Scrape(self.id, self.type).init_scrapping()

        # Store Scrapping log
        Scrapped().store_scrapped({
                "id": self.id,
                "type": self.type
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

        return scrapped_data