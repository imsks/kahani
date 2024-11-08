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
        
        return {
            "movie_id": self.id,
            "movie_data": scrapped_movie_details
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
    def get_movie_celebs(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        all_celeb_elements = soup.find_all('div', class_='credit_summary_item')
        
        celebs = []
        for celeb_element in all_celeb_elements:
            celeb = {}
            celeb_name = celeb_element.find('a')
            celeb_role = celeb_element.find('h4')
            
            if celeb_name and celeb_role:
                celeb['name'] = celeb_name.text.strip()
                celeb['role'] = celeb_role.text.strip()
                
                celebs.append(celeb)
                
        return celebs
    
    def get_scrapped_data(self):
        scrapped_data = self.init_scrapping()

        # Store Scrapping log
        Scrapped().store_scrapped({
                "id": self.id,
                "type": self.type
            })

        """
        // Movie
        id -> self.id
        name -> hero__primary-text
        description -> data-testid="plot"
        year -> hero-parent -> hero__pageTitle -> SIBLING -> UL
        link -> /title/{self.id}/
        type -> self.type
        rating -> hero-rating-bar__aggregate-rating__score
        runtime hero-parent -> hero__pageTitle -> SIBLING -> UL
        poster => ipc-media--poster-l
        celebs -> data-testid="title-cast"
        director -> data-testid="plot" -> SIBLING -> DIV
        writer -> data-testid="plot" -> SIBLING -> DIV
        genres -> data-testid="interests"

        // Celeb
        id
        name
        image
        """

        # return scrapped_data
        return {"scrapped_data": "scrapped_data"}
    
    # Helper functions
    def extract_year(text):
        # Matches a four-digit year
        match = re.match(r'^\d{4}$', text)
        return match.group(0) if match else None

    def extract_runtime(text):
        # Matches runtime format, e.g., '2h 39m'
        match = re.match(r'(\d+h\s*)?(\d+m)?', text)
        return text if match else None