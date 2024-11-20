import os
import re
from bs4 import BeautifulSoup
from database.models import Scrapped
from utils.api import APIUtils

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
        """
        // Movie
        director -> data-testid="title-pc-principal-credit" -> SIBLING -> DIV
        writer -> data-testid="title-pc-principal-credit" -> SIBLING -> DIV
        genres -> data-testid="interests"

        // Celeb
        id
        name
        image
        """

        soup = BeautifulSoup(html_content, 'html.parser')

        # Get movie name
        name = soup.find('span', class_='hero__primary-text').text

        # Get movie description
        description = soup.find('span', {'data-testid': 'plot-xs_to_m'}).text

        # Get movie year and runtime
        year = None
        runtime = None
        rating = None
        poster = None
        celeb_data = []
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
        poster_div = soup.find('div', class_='ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--rounded ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img')
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
                    celeb['image_url'] = self.get_hidef_image(image_tag)
                
                # Extract celeb name and ID from the anchor tag
                actor_tag = cast_item.find('a', {'data-testid': 'title-cast-item__actor'})
                if actor_tag:
                    celeb['name'] = actor_tag.get_text(strip=True)
                    
                    # Extract the ID from the href attribute
                    href = actor_tag['href']
                    celeb['id'] = href.split('/')[2] if '/name/' in href else None

                # Add celeb info to list if all required data is present
                if celeb:
                    celeb_data.append(celeb)

        # Get Movie Director & Writer
        credit_elements = soup.find_all('li', {'data-testid': 'title-pc-principal-credit'})

        # Initialize dictionaries for Director and Writer
        credits = {'Director': [], 'Writers': []}

        # Get first two elements only
        for element in credit_elements[0:2]:
            span = element.find('span', class_='ipc-metadata-list-item__label')
            if span and span.get_text(strip=True) in credits:
                credit_type = span.get_text(strip=True)

                content_div = element.find('div', class_='ipc-metadata-list-item__content-container')
                if content_div:
                    # Extract all names and IDs
                    anchor_tags = content_div.find_all('a', class_='ipc-metadata-list-item__list-content-item--link')
                    names_and_ids = []
                    for a in anchor_tags:
                        try:
                            # Extract and clean the name
                            name = " ".join(a.get_text().split()) if a.get_text() else "Unknown"
                            
                            # Extract the href and handle missing or malformed href attributes
                            href = a.get('href', '').split('?')[0]
                            if not href:
                                continue  # Skip if href is not available
                            
                            # Extract the ID safely
                            id = href.split('/')[2] if len(href.split('/')) > 2 else "Unknown"

                            # Append the name and ID
                            names_and_ids.append({'name': name, 'id': id})
                        except Exception as e:
                            # Log or handle unexpected issues gracefully
                            print(f"Error processing anchor tag: {a}, Error: {e}")
                    
                    # Add to credits
                    credits[credit_type].extend(names_and_ids)
                    
        return {
            "name": name,
            "description": ' '.join(description.split()),
            "year": year,
            "runtime": runtime,
            "link": f"https://www.imdb.com/title/{self.id}/",
            "type": self.type,
            "rating": rating,
            "poster": poster,
            "celebs": celeb_data,
            "credits": credits
        }
    
    def get_scrapped_data(self):
        scrapped_data = self.init_scrapping()

        # Store Scrapping log
        Scrapped().store_scrapped({
                "id": self.id,
                "type": self.type
            })
        
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
        srcset = img_tag.get('srcset', '')
                
        # Split srcSet by commas to get individual entries
        srcset_items = srcset.split(', ')
        
        # Take the last entry and split by space to get the URL part
        if srcset_items:
            poster = srcset_items[-1].split(' ')[0]
            return poster
        
        return None