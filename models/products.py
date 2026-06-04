from dataclasses import dataclass
from typing import List, ClassVar


@dataclass
class Product:
    ASIN: str
    title: str
    price: float
    list_price: float | None
    percentage_saving: float | None
    currency: str
    main_image_url: str
    detail_page_link: str
    video_link: str | None
    brand: str
    five_bullet_points: List[str]
    review_score: float
    review_count: int
    product_num: ClassVar[int] = 0

    def __post_init__(self):
        Product.product_num += 1