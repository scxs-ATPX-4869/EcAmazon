from bs4 import BeautifulSoup
from bs4.element import Tag
import re
from typing import List, Optional

from models.products import Product
from models.reviews import Review
from utils.utils import currency_symbol_to_code

class CenterCol:
    def __init__(
            self,
            centerCol_bs: BeautifulSoup | Tag
            ):
        self.centerCol_soup = centerCol_bs

    def brand(self) -> str:
        brand_tag = self.centerCol_soup.select_one("a#bylineInfo")
        visit_brand_store_str = brand_tag.get_text(strip=True)
        brand = re.match(r"Visit the (?P<brand>.*) Store", visit_brand_store_str)['brand']
        return brand

    def title(self) -> str:
        title_tag = self.centerCol_soup.select_one("span#productTitle")
        return title_tag.get_text(strip=True)

    def five_bullet_points(self) -> List[str]:
        bullet_points_block = self.centerCol_soup.select_one("div#feature-bullets") # there are at least 2 CSS selectors in 2026.1.31. This line is from a nail lamp
        bullet_points_container = bullet_points_block.find_all("li")
        return [bullet_point.get_text(strip=True) for bullet_point in bullet_points_container]

    def list_price(self) -> Optional[float]: # 当产品只有sale price没有list price时，缺少异常处理
        list_price_tag = self.centerCol_soup.select_one("div#corePriceDisplay_desktop_feature_div div.a-section.a-spacing-small.aok-align-center span.a-offscreen")
        list_price_str = list_price_tag.get_text(strip=True).replace(",", "") if list_price_tag else None
        if list_price_str:
            return float(list_price_str[1:])  # 去掉第一个字符（货币符号）
        
    def sale_price(self) -> float:
        price_tag = self.centerCol_soup.select_one("div#corePriceDisplay_desktop_feature_div span.priceToPay")
        price_str = price_tag.get_text(strip=True).replace(",", "")[1:]  # 去掉第一个字符（货币符号）
        return float(price_str)

    def percentage_saving(self) -> Optional[float]: # 当产品没有打折时，缺少异常处理
        percentage_saving_tag = self.centerCol_soup.select_one("div#corePriceDisplay_desktop_feature_div span.savingsPercentage")
        percentage_saving_str: str | None = percentage_saving_tag.get_text(strip=True)[1:] # 去掉第一个字符（百分号前的减号）
        return float(percentage_saving_str.strip("%")) if percentage_saving_str else None
    
    def coupon(self) -> Optional[float]: # 2026.1.31暂时只是获取优惠券tag的文本内容，未做进一步处理
        coupon_block = self.centerCol_soup.select_one("div.ct-coupon-tile-container")
        coupon_block_str: str = coupon_block.select_one("label.ct-coupon-checkbox-label").get_text(strip=True)
        return coupon_block_str
    
    def ratings(self) -> float:
        review_tag = self.centerCol_soup.select_one("span#acrPopover span.a-size-small.a-color-base")
        review_str = review_tag.get_text(strip=True)
        return float(review_str)
    
    def ratings_count(self) -> int:
        review_count_tag = self.centerCol_soup.select_one("span#acrCustomerReviewText")
        review_count_str = review_count_tag.get_text(strip=True).replace("()", "")
        return int(review_count_str)

class RightCol:
    def __init__(
            self,
            rightCol_bs: BeautifulSoup | Tag
            ):
        self.rightCol_soup = rightCol_bs

class LeftCol:
    def __init__(
            self,
            leftCol_bs: BeautifulSoup | Tag
            ):
        self.leftCol_soup = leftCol_bs

    def image_urls(self) -> List[str]:
        image_block = self.leftCol_soup.select_one("div#imageBlock")
        image_urls_tag = image_block.find_next_sibling("script", {"type": "text/javascript"})
        image_url_pattern = re.compile(r'''https://m\.media-amazon\.com/images/I/[^"]*_SL1500_\.jpg''')
        image_urls: List[str] = image_url_pattern.findall(image_urls_tag.get_text(strip=True))
        return image_urls

    def video_link(self) -> Optional[List[str]]:
        pass


class DetailPage:
    def __init__(
            self,
            dp_html: BeautifulSoup | Tag
            ):
        self.dp_soup = dp_html
        self._centerCol_cache: CenterCol | None = None
        self._rightCol_cache: RightCol | None = None
        self._leftCol_cache: LeftCol | None = None

    def _centerCol(self) -> CenterCol:
        self._centerCol_cache = CenterCol(self.dp_soup.select_one("div#centerCol"))
        return self._centerCol_cache

    def _rightCol(self) -> RightCol:
        self._rightCol_cache = RightCol(self.dp_soup.select_one("div#rightCol"))
        return self._rightCol_cache

    def _leftCol(self) -> LeftCol:
        self._leftCol_cache = LeftCol(self.dp_soup.select_one("div#leftCol"))
        return self._leftCol_cache
    
    def brand(self) -> str:
        if self._centerCol_cache is None:
            self._centerCol_cache = self._centerCol()
        return self._centerCol_cache.brand()
    
    def title(self) -> str:
        if self._centerCol_cache is None:
            self._centerCol_cache = self._centerCol()
        return self._centerCol_cache.title()
    
    def five_bullet_points(self) -> List[str]:
        if self._centerCol_cache is None:
            self._centerCol_cache = self._centerCol()
        return self._centerCol_cache.five_bullet_points()
    
    def sale_price(self) -> float:
        if self._centerCol_cache is None:
            self._centerCol_cache = self._centerCol()
        return self._centerCol_cache.sale_price()

    def list_price(self) -> Optional[float]:
        if self._centerCol_cache is None:
            self._centerCol_cache = self._centerCol()
        return self._centerCol_cache.list_price()

    def ratings(self) -> float:
        if self._centerCol_cache is None:
            self._centerCol_cache = self._centerCol()
        return self._centerCol_cache.ratings()

    def ratings_count(self) -> int:
        if self._centerCol_cache is None:
            self._centerCol_cache = self._centerCol()
        return self._centerCol_cache.ratings_count()

    def ac_badge(self) -> Optional[list[str]]:
        pass

    def top_highlights(self) -> Optional[dict[str, str]]: # 用 B0CN2RXGRJ 去测试
        pass

    def product_features_overview(self) -> Optional[dict[str, str]]: # 用 B0DMJJQLXW 去测试
        pass

    def variations(self) -> Optional[dict]: # 用 B0DMJJQLXW 去测试
        pass

    def picture_urls(self) -> List[str]:
        pass

    def video_links(self) -> Optional[str]:
        pass

    def product_information(self) -> Optional[dict[str, str]]: # 用 B0DMJJQLXW 去测试
        pass

    def product_details(self) -> Optional[dict[str, str]]: # 用 B0CN2RXGRJ 去测试
        pass

    def product_description(self) -> Optional[str]: # 用 B0CN2RXGRJ 去测试
        pass

    def Prime_A_Plus(self) -> Optional[dict]:
        pass

    def reviews(self) -> Review: # 评论的专门链接：https://www.amazon.com/product-reviews/{ASIN}
        pass