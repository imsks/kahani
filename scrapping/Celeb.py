from bs4 import BeautifulSoup
from database.models import Movie, MovieCelebRole, Scrapped
from utils.api import APIUtils
from utils.contants import CelebRoles, SearchItemType

class CelebScrapper:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    # Init Scrapping
    def init_scrapping(self):
        scrapped_celeb_details = self.scrape_celeb_details()
        celeb_filmography = self.get_celeb_filmography(scrapped_celeb_details)

        return {
            "celeb_id": self.id,
            "celeb_filmography": celeb_filmography,
        }
    
    # Build celeb URL
    def build_celeb_url(self):
        url = "https://www.imdb.com/name/" + self.id
        
        return url
    
    # Scrape celeb Details
    def scrape_celeb_details(self):
        url = self.build_celeb_url()
        response = APIUtils.make_api(url)
        
        return response.content
    
    # Get Celeb Filmography
    def get_celeb_filmography(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        all_writer_elements = soup.find('div', id='accordion-item-writer-previous-projects')
        all_producer_elements = soup.find('div', id='accordion-item-producer-previous-projects')
        all_director_elements = soup.find('div', id='accordion-item-director-previous-projects')
        all_actor_elements = soup.find('div', id='accordion-item-actor-previous-projects')

        writer_films = self.process_film_details(all_writer_elements)
        producer_films = self.process_film_details(all_producer_elements)
        director_films = self.process_film_details(all_director_elements)
        actor_films = self.process_film_details(all_actor_elements)

        return {
            "writer": writer_films,
            "producer": producer_films,
            "director": director_films,
            "actor": actor_films
        }

    # Process Film Details
    def process_film_details(self, all_films_element):
        films = []

        if not all_films_element:
            return films

        film_elements = all_films_element.find_all('li')

        for film_element in film_elements:
            link = film_element.find('a', class_='ipc-metadata-list-summary-item__t')
            rating = film_element.find('span', class_='ipc-rating-star')

            film  = {}

            if link and rating:
                film['rating'] = rating.text.strip()
                name  = link.text.strip()
                film['name'] = name

                anchor = link.get('href').split('?')[0]
                if anchor:
                    film['link'] = anchor
                    film['id'] = anchor.split('/')[2]
                
                image = film_element.find('img', class_='ipc-image')

                if image:
                    film['image'] = image.get('src')
                else:
                    film['image'] = ""

                year = film_element.find('span', class_='ipc-metadata-list-summary-item__li')
                
                film['year'] = year.text.strip() if year else ""

                info_span = film_element.find('div', class_='ipc-metadata-list-summary-item__tc')
                info_span_values = info_span.find('div').find_all('span')[-1]

                type = SearchItemType.MOVIE.value
                for value in info_span_values:
                    if value.get_text() == 'TV Series':
                        type = SearchItemType.TV_SHOW.value
                        break

                film['type'] = type
                    
                films.append(film)
                
        return films
    
    def get_scrapped_data(self):
        scrapped_data = self.init_scrapping()

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
    