import requests

from utils.api import APIUtils
from utils.contants import SearchItemType

class Search:
    def __init__(self, query):
        self.query = query

    def get_query_suggestions(self):
        # Scrape the celeb details
        query_suggestions = SearchIMDB(self.query).fetch_query_suggestions()

        return query_suggestions
    
# Search IMDB
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
        print(query_suggestions)

        if not query_suggestions:
            return []
        
        mapped_query_suggestions = []

        for suggestion in query_suggestions:
            type = ''
            is_valid = False

            if suggestion.get('qid', '') == '':
                type = SearchItemType.CELEB.value
                is_valid = True
            elif suggestion.get('qid', '') == 'tvSeries':
                type = SearchItemType.TV_SHOW.value
                is_valid = True
            elif suggestion.get('qid', '') == 'movie':
                type = SearchItemType.MOVIE.value
                is_valid = True

            if is_valid:
                mapped_query_suggestions.append(
                    {
                        "id": suggestion.get('id', ''),
                        "name": suggestion.get('l', ''),
                        "image": suggestion.get('i', {}).get('imageUrl', None),
                        "type": type, 
                        "year": suggestion.get('y'),
                    }
                )

        # scraped_celeb_details = ScrapeCeleb().init_scrapping(mapped_query_suggestions[0]['id'])

        return mapped_query_suggestions