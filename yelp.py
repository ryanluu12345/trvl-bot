import requests
import json
import os
from dotenv import load_dotenv

class Yelp:
    def __init__(self):
        self.base_url = 'https://api.yelp.com/v3/businesses/search'
        self.default_params = {'term': 'coffee',
                               'location': 'Toronto, Ontario',
                               'limit': 5}
        self.api_key = os.getenv('YELP_KEY')
        self.headers = {'Authorization': 'Bearer {}'.format(self.api_key)}
        self.businesses_cache = {} # Holds the latest businesses requested

    def get_businesses(self, term = None, location = None, limit = None):
        # Naive approach: refresh cache everytime a new set of data is requested from API
        self.businesses_cache = {}

        self.params = {
            "term" : term if term else self.default_params["term"],
            "location" : location if location else self.default_params["location"],
            "limit" : limit if limit else self.default_params["limit"]
        }

        # TODO: error handling
        response = requests.get(
        self.base_url, headers=self.headers, params=self.params, timeout=5)
        
        # Store in the cache so we can get more details if requested
        for business in response.json()["businesses"]:
            self.businesses_cache[business["name"]] = business

        print(json.dumps(response.json(), indent=4))
        return self.businesses_cache
        


if __name__ == "__main__":
    load_dotenv()
    yelp = Yelp()
    yelp.get_businesses("coffee", "New York")
