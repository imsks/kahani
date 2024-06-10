from utils import ScrapeCeleb

class Scrapper:
    def __init__(self, query):
        self.query = query

    def init_scrapping(self):
        # Scrape the celeb details
        celeb = ScrapeCeleb(self.query, self)
