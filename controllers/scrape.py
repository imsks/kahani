from utils.api import APIUtils
from bs4 import BeautifulSoup
from utils.api import APIUtils
from utils.contants import SearchItemType

class Scrape:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def init_scrapping(self):
        if self.type == SearchItemType.MOVIE.value:
            return None
        elif self.type == SearchItemType.CELEB.value:
            return ScrapeCeleb(self.id).init_scrapping()
        else:
            return {
                "error": "Invalid type"
            }

# Scrap Celebs
class ScrapeCeleb:
    def __init__(self, id):
        self.id = id
        
    # Init Scrapping
    def init_scrapping(self):
        scrapped_celeb_details = self.scrape_celeb_details()
        celeb_filmography = self.get_celeb_filmography(scrapped_celeb_details)

        return {
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

            film  = {}

            if link:
                title  = link.text.strip()
                film['title'] = title

                anchor = link.get('href').split('?')[0]
                if anchor:
                    film['link'] = anchor

                rating = film_element.find('span', class_='ipc-rating-star')

                if rating:
                    film['rating'] = rating.text.strip()
                else:
                    film['rating'] = ""

                cover = film_element.find('img', class_='ipc-image')

                if cover:
                    film['cover'] = cover.get('src')
                else:
                    film['cover'] = ""
                    
                films.append(film)

        return films