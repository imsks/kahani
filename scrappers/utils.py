import json
from bs4 import BeautifulSoup
import requests
from utils.api import APIUtils

# Scrap Class
class ScrapeCeleb:
    def __init__(self, query, role):
        self.query = query
        self.role = role

    # Init Scrapping
    def init_scrapping(self):
        pre_scrapper = SearchIMDB(self.query)

        response = pre_scrapper.make_imdb_suggestion_api()

        parsed_celeb = self.parse_imdb_suggestions(response)

        scrapped_celeb_details = self.scrape_celeb_details(parsed_celeb['id'])

        celeb_filmography = self.get_celeb_filmography(scrapped_celeb_details)

        return {
            "celeb_name": parsed_celeb['l'],
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

class SearchIMDB:
    def __init__(self, query):
        self.query = query
        
    # Build IMDB Suggestion URL
    def build_imdb_suggestion_url(self):
        # Encode the search query for safe inclusion in the URL
        encoded_query = requests.utils.quote(self.query)
        
        # Base URL for IMDB suggestion API
        base_url = "https://v3.sg.media-imdb.com/suggestion/x/"
        
        # Construct the final URL with encoded query
        url = base_url + encoded_query + ".json" + "?includeVideos=1"
        
        return url
    
    # Make IMDB Suggestion API
    def make_imdb_suggestion_api(self):
        url = self.build_imdb_suggestion_url()
        response = APIUtils.make_api(url)
        
        return APIUtils.check_response(response)
    
    # Parse IMDB Suggestion API Response
    def parse_imdb_suggestions(self, api_response):
        if "d" not in api_response:
            return None  # Handle invalid response (missing "d" key)

        # Get the list of suggestions from the "d" key
        suggestions = api_response["d"]
        
        # Check if there are any suggestions
        if not suggestions:
            return None  # No suggestions found

        # Return the first suggestion (assuming the list is not empty)
        return suggestions
    
    # Fetch Query Suggestions
    def fetch_query_suggestions(self):
        response = self.make_imdb_suggestion_api()

        query_suggestions = self.parse_imdb_suggestions(response)

        if not query_suggestions:
            return []
        
        mapped_query_suggestions = []

        for suggestion in query_suggestions:
            mapped_query_suggestions.append(
                {
                    "id": suggestion.get('id', ''),
                    "name": suggestion.get('l', ''),
                    "image": suggestion.get('i', {}).get('imageUrl', None),
                    "type": suggestion.get('q', ''),
                    "typeId": suggestion.get('qid', ''), 
                    "year": suggestion.get('y', ''),
                }
            )

        return mapped_query_suggestions