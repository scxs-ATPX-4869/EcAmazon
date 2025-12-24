import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag


class ListItem:
    def __init__(self, item: BeautifulSoup | Tag):
        pass

class SearchResult:
    def __init__(
            self,
            search_term: str,
            headers: dict | None = None,
            ):
        self.client = httpx.Client(
            base_url="https://www.amazon.com/s",
            params={"k": SearchResult.build_search_term(search_term)},
            headers=headers,
            timeout=30,
        )
    

    @staticmethod
    def build_search_term(*args: str) -> str:
        return " ".join(args).strip().replace(" ", "+")
    
    def main_imges(self) -> list:
        pass

    def product_links(self) -> list:
        pass

    def product_titles(self) -> list:
        pass



















if __name__ == "__main__":
    sr = SearchResult("nikon z6iii")
    
