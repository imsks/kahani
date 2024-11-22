import os
import re
from bs4 import BeautifulSoup
from database.models import Celeb, Movie, Scrapped
from utils.api import APIUtils
from utils.contants import SearchItemType

class MovieScrapper:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def get_or_create_html_file(self):
        # Define the filename based on the movie ID (to uniquely identify each movie)
        filename = f"movie_{self.id}.html"
        
        # Check if the HTML file exists
        if os.path.exists(filename):
            print("HTML file already exists. Loading data from the file.")
            with open(filename, "r", encoding="utf-8") as file:
                return file.read()  # Return the existing HTML data
        
        # If the file doesn't exist, scrape the data
        scrapped_movie_details = self.scrape_movie_details()
        
        # If scrapped_movie_details is bytes, decode it to string
        if isinstance(scrapped_movie_details, bytes):
            scrapped_movie_details = scrapped_movie_details.decode("utf-8")
        
        # Save the scrapped data as an HTML file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(scrapped_movie_details)
        
        print("HTML file created and data saved.")
        return scrapped_movie_details  # Return the freshly scraped data

    # Init Scrapping
    def init_scrapping(self):
        # TODO: Implement the logic to scrape movie details
        # scrapped_movie_details = self.scrape_movie_details()
        scrapped_movie_details = self.get_or_create_html_file()
        movie_data = self.process_film_content(scrapped_movie_details)
        
        return {
            "id": self.id,
            **movie_data
        }
    
    # Build movie URL
    def build_movie_url(self):
        url = "https://www.imdb.com/title/" + self.id
        
        return url
    
    # Scrape movie Details
    def scrape_movie_details(self):
        url = self.build_movie_url()
        response = APIUtils.make_api(url)
        
        return response.content
    
    # Get Movie Celebs
    def process_film_content(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get movie name
        name = soup.find('span', class_='hero__primary-text').text

        # Get movie description
        description = soup.find('span', {'data-testid': 'plot-xs_to_m'}).text
        description = ' '.join(description.split())

        # Get Movie link
        link = f"https://www.imdb.com/title/{self.id}/"

        # Get movie year and runtime
        year = None
        runtime = None
        rating = None
        poster = None
        celeb_data = []
        credits = {'Directors': [], 'Writers': []}
        genres = []

        section = soup.find('section', {'data-testid': 'hero-parent'})
        if section:
            page_title_h1 = section.find('h1', {'data-testid': 'hero__pageTitle'})

            if page_title_h1:
                # Find the ul with class "ipc-inline-list" and each li within it
                ul = page_title_h1.find_next_sibling('ul', class_='ipc-inline-list')
                
                if ul:
                    li_elements = ul.find_all('li', class_='ipc-inline-list__item')
                    li_texts = [li.get_text(strip=True) for li in li_elements]
                    
                    # Process each li element to extract year and runtime
                    for text in li_texts:
                        if not year:
                            year = self.extract_year(text)
                        elif not runtime:
                            runtime = self.extract_runtime(text)
        
        # Get Movie Rating
        rating_div = soup.find('div', {"data-testid": 'hero-rating-bar__aggregate-rating__score'})
        if rating_div:
            rating_span = rating_div.find('span')  # Target the first span
            if rating_span:
                rating = rating_span.get_text(strip=True)

        # Get Movie Poster
        poster_div = soup.find('div', {"data-testid": 'hero-media__poster'})
        if poster_div:
            img_tag = poster_div.find('img')
            if img_tag:
                poster = self.get_hidef_image(img_tag)

        # Get Movie Cast
        cast_section = soup.find('section', {'data-testid': 'title-cast'})
        # Process only the first five celeb items
        if cast_section:
            cast_items = cast_section.find_all('div', {'data-testid': 'title-cast-item'}, limit=5)
            
            for cast_item in cast_items:
                celeb = {}

                # Extract image URL (last item in srcSet)
                image_tag = cast_item.find('img', {'class': 'ipc-image'})
                if image_tag and image_tag.has_attr('srcset'):
                    celeb['image'] = self.get_hidef_image(image_tag)
                
                # Extract celeb name and ID from the anchor tag
                actor_tag = cast_item.find('a', {'data-testid': 'title-cast-item__actor'})
                if actor_tag:
                    celeb['name'] = actor_tag.get_text()
                    
                    # Extract the ID from the href attribute
                    href = actor_tag['href']
                    celeb['id'] = href.split('/')[2] if '/name/' in href else None

                # Add celeb info to list if all required data is present
                if celeb:
                    celeb_data.append(celeb)

        # Get Movie Director & Writer
        credit_elements = soup.find_all('li', {'data-testid': 'title-pc-principal-credit'})

        # Get first two elements only
        for element in credit_elements[0:2]:
            span = element.find('span', class_='ipc-metadata-list-item__label')
            if span and span.get_text(strip=True):
                credit_type = span.get_text(strip=True)

                # If credit_type is Director or Directors, make it Directors same for Writers
                if credit_type == 'Director':
                    credit_type = 'Directors'
                elif credit_type == 'Writer':
                    credit_type = 'Writers'

                content_div = element.find('div', class_='ipc-metadata-list-item__content-container')
                if content_div:
                    # Extract all names and IDs
                    anchor_tags = content_div.find_all('a', class_='ipc-metadata-list-item__list-content-item--link')
                    names_and_ids = []
                    for a in anchor_tags:
                        try:
                            # Extract and clean the name
                            celeb_name = " ".join(a.get_text().split()) if a.get_text() else "Unknown"
                            
                            # Extract the href and handle missing or malformed href attributes
                            href = a.get('href', '').split('?')[0]
                            if not href:
                                continue  # Skip if href is not available
                            
                            # Extract the ID safely
                            id = href.split('/')[2] if len(href.split('/')) > 2 else "Unknown"

                            # Append the name and ID
                            names_and_ids.append({'name': celeb_name, 'id': id})
                        except Exception as e:
                            # Log or handle unexpected issues gracefully
                            print(f"Error processing anchor tag: {a}, Error: {e}")
                    
                    # Add to credits
                    credits[credit_type].extend(names_and_ids)
                    
        # Find the parent div with data-testid="interests"
        genres_div = soup.find('div', {'data-testid': 'interests'})        

        # Check if the parent div exists
        if genres_div:
            # Find the scroller div
            scroller_div = genres_div.find('div', class_='ipc-chip-list__scroller')
            
            if scroller_div:
                # Find all span elements with class 'ipc-chip__text'
                span_elements = scroller_div.find_all('span', class_='ipc-chip__text')
                
                # Extract and clean the text from each span
                genres = [span.get_text(strip=True) for span in span_elements]

        return {
            "name": name,
            "description": description,
            "year": year,
            "runtime": runtime,
            "link": link,
            "type": self.type,
            "rating": rating,
            "poster": poster,
            "celebs": celeb_data,
            "credits": credits,
            "genres": genres
        }
    
    def get_scrapped_data(self):
        scrapped_data = self.init_scrapping()

        # Store Scrapping log
        Scrapped().store_scrapped({
                "id": self.id,
                "type": self.type
            })
        
        # Store Data in Movies Model
        movie = {
            "id": self.id,
            "name": scrapped_data.get('name'),
            "description": scrapped_data.get('description'),
            "year": scrapped_data.get('year'),
            "runtime": scrapped_data.get('runtime'),
            "link": scrapped_data.get('link'),
            "type": scrapped_data.get('type'),
            "rating": scrapped_data.get('rating'),
            "poster": scrapped_data.get('poster'),
            "credits": scrapped_data.get('credits'),
            "genres": scrapped_data.get('genres'),
            "celebs": scrapped_data.get('celebs')
        }

        Movie().store_movie(movie)
        
        # return scrapped_data
        return scrapped_data
    
    # Helper functions
    def extract_year(self, text):
        if text.isdigit() and len(text) == 4:
            return text
        return None

    def extract_runtime(self, text):
        # Check if the text has a time-related keyword (e.g., 'min')
        if 'm' in text or 'h' in text:
            return text
        return None
    
    def get_hidef_image(self, img_tag):
        # Extract the srcset attribute from the img tag
        srcset = img_tag.get('srcset', '')
        
        if not srcset:  # If srcset is missing or empty, return None
            return None
        
        # Split srcset by commas to get individual entries
        srcset_items = srcset.split(', ')
        
        # Ensure there are items to process
        if srcset_items:
            # Take the last entry, strip whitespace, and split to isolate the URL
            all_items = srcset_items[-2].strip().split(' ')

            if all_items:
                return all_items[0]
        
        return None
