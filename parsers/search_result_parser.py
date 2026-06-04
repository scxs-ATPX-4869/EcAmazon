from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List

from models.products import Product
from utils.utils import currency_symbol_to_code

class ListItem:
    def __init__(
            self,
            product_item: BeautifulSoup | Tag
            ):
        self.soup = product_item
        self.asin: str | None = None

    def ASIN(self) -> str:
        if self.asin:
            return self.asin
        else:
            self.asin = self.soup.get("data-asin")
            return self.asin

    def currency(self) -> str:
        currency = self.soup.select_one("span.a-price > span.a-offscreen").get_text(strip=True)
        return currency_symbol_to_code(currency[0]) # currency[0]: 取第一个字符作为货币符号

    def price(self) -> float:
        price = self.soup.select_one("span.a-price > span.a-offscreen").get_text(strip=True)
        return float(price[1:].replace(",", ""))  # price[1:]: 去掉第一个字符（货币符号）; 再去掉千分位逗号

    def title(self) -> str:
        title = self.soup.select_one("a.a-link-normal.a-text-normal span").get_text(strip=True)
        return title

    def main_image_url(self) -> str:
        image_url = self.soup.select_one("div.a-section.aok-relative.s-image-fixed-height > img").get("src")
        return image_url

    def detail_page_link(self) -> str:
        if self.asin:
            return f"https://www.amazon.com/dp/{self.asin}"
        else:
            self.ASIN()
            return f"https://www.amazon.com/dp/{self.asin}"

    def review_score(self) -> float:
        rating = self.soup.select_one("span.a-size-small.a-color-base").get_text(strip=True)
        return float(rating)

    def review_count(self) -> int:
        count = self.soup.select_one("span.a-size-mini.puis-normal-weight-text.s-underline-text").get_text(strip=True)
        return int(count.strip("()"))
    
    def product(self) -> Product:
        return Product(
            ASIN=self.ASIN(),
            title=self.title(),
            price=self.price(),
            currency=self.currency(),
            main_image_url=self.main_image_url(),
            detail_page_link=self.detail_page_link(),
            review_score=self.review_score(),
            review_count=self.review_count(),
        )
    

class SearchResult:
    def __init__(
            self,
            html: str,
            ):
        self.soup = BeautifulSoup(html, "html.parser")
        self.items_list: List[ListItem] = list()

    def _items(self) -> List[ListItem]:
        search_result_items_container = self.soup.find("div", {"class": "s-main-slot s-result-list s-search-results sg-row"})
        product_items = search_result_items_container.find_all("div", {"data-component-type": "s-search-result"})
        return [ListItem(item) for item in product_items]
    
    def products(self) -> List[Product]:
        return [item.product() for item in self._items()]

    def __len__(self) -> int:
        return len(self.items_list)