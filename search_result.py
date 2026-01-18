import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag


class ListItem:
    def __init__(self, item: BeautifulSoup | Tag):
        self.soup = item
        self.asin: str | None = None

    def price(self) -> float:
        price = self.soup.select_one("span.a-price > span.a-offscreen").get_text(strip=True)
        return float(price.replace("$", "").replace(",", ""))
    
    def currency(self) -> str:
        currency = self.soup.select_one("span.a-price > span.a-offscreen").get_text(strip=True)
        return ListItem._currency_symbol_to_code(currency[0])

    def title(self) -> str | None:
        title = self.soup.select_one("a.a-link-normal.a-text-normal span").get_text(strip=True)
        return title

    def main_image_url(self) -> str | None:
        image_url = self.soup.select_one("div.a-section.aok-relative.s-image-fixed-height > img").get("src")
        return image_url

    def link(self) -> str | None:
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

    def ASIN(self) -> str:
        if self.asin:
            return self.asin
        else:
            asin = self.soup.get("data-asin")
            self.asin = asin
            return asin
    
    @staticmethod
    def _currency_symbol_to_code(symbol: str) -> str:
        currency_map = {
            "$": "USD",
            "£": "GBP",
            "€": "EUR",
            "¥": "JPY",
            "₹": "INR",
        }
        return currency_map.get(symbol, symbol)

class SearchResult:
    def __init__(
            self,
            search_iterm: str,
            headers: dict | None = None,
            ):
        self.client = httpx.Client(
            base_url="https://www.amazon.com",
            headers=headers,
            cookies={"ubid-main": "132-1234567-1234567"},
            timeout=30,
        )
        self.search_item = search_iterm
        self.response = self.client.get(url="/s", params={"k": SearchResult._build_search_term(search_iterm)})
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    @staticmethod
    def _build_search_term(*args: str) -> str:
        return " ".join(args).strip().replace(" ", "+")
    
    def search_items_list(self) -> list[ListItem]:
        search_result = self.soup.find("div", {"class": "s-main-slot s-result-list s-search-results sg-row"})
        items = search_result.find_all("div", {"role": "listitem"})
        return [ListItem(item) for item in items]
    
    def result_html(self):
        with open(f"search_result-{SearchResult._build_search_term(self.search_item)}.html", "w", encoding="utf-8") as f:
            f.write(self.soup.prettify())
    
    def close(self):
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        





if __name__ == "__main__":
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "referer": "https://www.amazon.com/",
    }
    with SearchResult("nikon z6iii", headers=headers) as sr:
        items = sr.search_items_list()
        print(len(items))
        item = items[0]

        title = item.title()
        print(title)
        print(type(title))

        price = item.price()
        print(price)
        print(type(price))

        currency = item.currency()
        print(currency)
        print(type(currency))

        main_image_url = item.main_image_url()
        print(main_image_url)
        print(type(main_image_url))



        reviews_score = item.review_score()
        print(reviews_score)
        print(type(reviews_score))

        reviews_count = item.review_count()
        print(reviews_count)
        print(type(reviews_count))

        asin = item.ASIN()
        print(asin)
        print(type(asin))

        product_link = item.link()
        print(product_link)
        print(type(product_link))




    
