from dataclasses import dataclass
from typing import ClassVar, List, Optional

@dataclass
class Review:
    ASIN: str
    review_date: str
    review_country: str
    review_title: str
    review_content: str
    review_rating: float
    review_helpful_votes: int
    review_images: List[str]
    review_videos: List[str]