import requests
from requests import Response

from utils.utils import combine_key_words

class AmazonClient:
    def __init__(self, session: requests.Session):
        self.session = session

    def detail_product(self, ASIN: str):
        url = f"https://www.amazon.com/dp/{ASIN}"
        response: Response = self.session.get(url)
        if response.ok:
            return response.text
        else:
            raise Exception(f"Failed to fetch product details for ASIN {ASIN}. Status code: {response.status_code}")
        
    def search_result(self, keywords: str, page: int = 1):
        keyword = combine_key_words(keywords)
        url = f"https://www.amazon.com/s?k={keyword}&page={page}"
        response: Response = self.session.get(url)
        if response.ok:
            return response.text
        else:
            raise Exception(f"Failed to fetch search results for keyword '{keyword}' on page {page}. Status code: {response.status_code}")