from controllers.scrape import Scrape
from database.models import Movie, MovieCelebRole, Scrapped
from utils.contants import CelebRoles

class MovieScrapper:
    def __init__(self, id, type):
        self.id = id
        self.type = type
    
    def init_scrapping(self):
        scrapped_data = Scrape(self.id, self.type).init_scrapping()

        return scrapped_data
    
# Scrap Movies
class ScrapeMovie:
    def __init__(self, id):
        self.id = id
        
    # Init Scrapping
    def init_scrapping(self):
        scrapped_movie_details = self.scrape_movie_details()
        movie_celebs = self.get_movie_celebs(scrapped_movie_details)
        
        return {
            "movie_id": self.id,
            "movie_celebs": movie_celebs,
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