from dataclasses import dataclass
from typing import ClassVar, List, Optional

@dataclass
class APlus:
    ASIN: str
    QA: Optional[dict[str, str]]
    product_pictures: Optional[dict]