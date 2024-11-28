from bs4 import BeautifulSoup
from database.models import Celeb, Movie, MovieCelebRole, Scrapped
from utils.api import APIUtils
from utils.contants import CelebRoles, SearchItemType
from utils.functions import get_hidef_image


class CelebScrapper:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    # Init Scrapping
    def init_scrapping(self):
        scrapped_celeb_details = self.scrape_celeb_details()
        celeb = self.get_celeb_filmography(scrapped_celeb_details)

        return {
            "id": self.id,
            **celeb,
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

        try:
            name = soup.find('span', {"data-testid": "hero__primary-text"}).text.strip()
        except AttributeError:
            name = ''
        image = ""

        # Display Picture
        hero_container = soup.find('section', {"data-testid": 'hero-parent'})

        if hero_container:
            img_tag = hero_container.find('img', class_='ipc-image')

            if img_tag:
                image = get_hidef_image(img_tag)
                    
        return {
            "filmography": {
                "actor": actor_films,
                "writer": writer_films,
                "director": director_films,
                "producer": producer_films
            },
            "image": image,
            "name": name
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
                film['name'] = f"https://www.imdb.com/title/{name}/"

                anchor = link.get('href').split('?')[0]
                if anchor:
                    film['link'] = anchor
                    film['id'] = anchor.split('/')[2]
                
                poster = film_element.find('img', class_='ipc-image')

                if poster:
                    film['poster'] = poster.get('src')
                else:
                    film['poster'] = ""

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
        id = scrapped_data.get('id')
        celeb_filmography = scrapped_data.get('filmography')
        
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
                    MovieCelebRole().store_movie_celeb_role(movie.get('id'), id, celeb_role_enum.value)

        # Store Celeb Image
        celeb_data = {
            "id": id,
            "name": scrapped_data.get('name'),
            "image": scrapped_data.get('image')
        }
        celeb = Celeb().store_celeb({**celeb_data, "type": CelebRoles.ACTOR.value})

        return scrapped_data
    