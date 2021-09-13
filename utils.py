"""Commonly used utilities"""

from multiprocessing.pool import ThreadPool
from PIL import ImageFile
import re
from typing import List, Optional
from urllib.request import urlopen

from bs4 import BeautifulSoup
import requests

from article import Image


def normalize_text(text: str) -> str:
    return ' '.join(text.split('\n'))


def fetch_image_dimensions(url: str) -> Optional[Image]:
    """Fetches the dimensions of an image without downloading it."""
    try:
        file = urlopen(url)
    except Exception as e:
        pass
    else:
        p = ImageFile.Parser()
        while True:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                file.close()
                return Image(url, p.image.size)
        file.close()


def fetch_images_dimensions(image_urls: List[str]) -> List[Optional[Image]]:
    """Fetches the dimensions for a given batch of image urls"""
    return [
        result for result in ThreadPool(20).imap_unordered(
            fetch_image_dimensions, image_urls) if result
    ]


def filter_images(images: List[Image]) -> List[Image]:
    """Filters images"""
    filtered_by_size = size_filter(images)
    return filtered_by_size


def size_filter(images: List[Image],
                widht: int = 25,
                height: int = 25) -> List[Image]:
    """Filters those images having width and height less than the specified"""
    return [
        image for image in images
        if image.dimensions[0] >= widht and image.dimensions[1] >= height
    ]


def sort_by_dims(images: List[Image]) -> List[Image]:
    """Sorts the list of images by dimensions"""
    return sorted(images,
                  key=lambda image:
                  (image.dimensions[0] * image.dimensions[1]),
                  reverse=True)


def scrap_image_urls(url: str) -> List[str]:
    """Fetches all supported image format(JPG,PNG and JPEG) present on a URL"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')
    regex = "(?P<url>https?://[^\s]+)"
    urls = [
        re.search(regex, str(url)).group("url").rstrip('"') for url in images
        if re.search(regex, str(url))
    ]
    return list(
        filter(lambda url: 'jpg' in url or 'jpeg' in url or 'png' in url,
               urls))
