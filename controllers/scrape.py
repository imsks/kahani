from scrapping.Celeb import CelebScrapper
from utils.contants import SearchItemType

class ScrapeController:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def main(self):
        if self.type == SearchItemType.CELEB.value:
            return CelebScrapper(self.id, self.type).get_scrapped_data()
        elif self.type == SearchItemType.MOVIE.value or self.type == SearchItemType.TV_SHOW.value:
            return CelebScrapper(self.id, self.type).get_scrapped_data()
        else:
            return {
                "error": "Invalid type"
            }

    
