from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime


@dataclass(frozen=True)
class Article_MetaData:
    title: str
    url: str
    date_published: datetime


@dataclass(frozen=True)
class Image:
    url: str
    dimensions: Tuple[int, int]  # (Width, Height)


@dataclass(frozen=True)
class Article:
    meta: Article_MetaData
    summary: str
    images: List[Image] = field(default_factory=list,
                                hash=False,
                                compare=False)
