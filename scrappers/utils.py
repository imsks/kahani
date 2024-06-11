from bs4 import BeautifulSoup
from utils.api import APIUtils

# Scrap Celebs
class ScrapeCeleb:
    # Init Scrapping
    def init_scrapping(self, celeb_id):
        scrapped_celeb_details = self.scrape_celeb_details(celeb_id)

        celeb_filmography = self.get_celeb_filmography(scrapped_celeb_details)

        return {
            "celeb_filmography": celeb_filmography,
        }
    
    # Build celeb URL
    def build_celeb_url(self, celeb_id):
        url = "https://www.imdb.com/name/" + celeb_id
        
        return url
    
    # Scrape celeb Details
    def scrape_celeb_details(self, celeb_id):
        url = self.build_celeb_url(celeb_id)
        response = APIUtils.make_api(url)
        
        return response.content
    
    # Get Celeb Filmography
    def get_celeb_filmography(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        all_writer_elements = soup.find('div', id='accordion-item-writer-previous-projects')
        all_producer_elements = soup.find('div', id='accordion-item-producer-previous-projects')
        all_director_elements = soup.find('div', id='accordion-item-director-previous-projects')

        writer_films = self.process_film_details(all_writer_elements)
        producer_films = self.process_film_details(all_producer_elements)
        director_films = self.process_film_details(all_director_elements)

        return {
            "writer": writer_films,
            "producer": producer_films,
            "director": director_films
        }

    # Process Film Details
    def process_film_details(self, all_films_element):
        if not all_films_element:
            return {
                "titles": [],
                "links": [],
                "covers": [],
                "ratings": []
            }

        titles = []
        links = []
        covers = []
        ratings = []

        film_elements = all_films_element.find_all('li')

        for film_element in film_elements:
            link = film_element.find('a', class_='ipc-metadata-list-summary-item__t')

            if link:
                title  = link.text.strip()
                titles.append(title)

                anchor = link.get('href').split('?')[0]
                if anchor:
                    links.append(anchor)

                rating = film_element.find('span', class_='ipc-rating-star')

                if rating:
                    ratings.append(rating.text.strip())
                else:
                    ratings.append("") 

                cover = film_element.find('img', class_='ipc-image')

                if cover:
                    covers.append(cover.get('src'))
                else:
                    covers.append("") 

        # Find the maximum length of any list
        max_length = max(len(lst) for lst in [titles, links, covers, ratings])

        # Pad shorter lists with empty strings
        for lst in [titles, links, covers, ratings]:
            lst.extend([""] * (max_length - len(lst)))

        return {
            "titles": titles,
            "links": links,
            "covers": covers,
            "ratings": ratings
        }