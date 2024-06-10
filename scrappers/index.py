from .utils import SearchIMDB

class Search:
    def __init__(self, query):
        self.query = query

    def get_query_suggestions(self):
        # Scrape the celeb details
        query_suggestions = SearchIMDB(self.query).fetch_query_suggestions()

        return query_suggestions