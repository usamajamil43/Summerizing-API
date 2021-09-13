"""Implements functionality to scrap news articles urls for article's text and images.
Summarizes the text before storing
"""
from typing import List

from newspaper import Article as news_article

from article import Article, Article_MetaData, Image
from utils import normalize_text
from utils import fetch_images_dimensions
from utils import filter_images
from utils import sort_by_dims
from utils import scrap_image_urls
from scrap_error import ScrapError


class ArticleScrapper:
    def __init__(self) -> None:
        pass

    def __make_images(self, image_urls: List[str]) -> List[Image]:
        """Fetches dimensions of images, filters and sort them wrt to pixel density"""
        images = fetch_images_dimensions(image_urls)
        images = filter_images(images)
        images = sort_by_dims(images)
        return images

    def __fetch_article(self, meta: Article_MetaData,
                        scrap_images: bool) -> Article:
        """Fetches the text and images for a single article."""
        article = news_article(meta.url)
        article.download()
        try:
            article.parse()
            article.nlp()
            summary = normalize_text(article.summary)
            images = []

            if scrap_images:
                image_urls = scrap_image_urls(meta.url)
                images = self.__make_images(image_urls)
            return Article(meta, summary=summary, images=images)

        except Exception as e:
            raise ScrapError(
                f'Article URL could not be scrapped: {meta.url}\nError: {e}')

    def fetch_articles_batch(self,
                             metadatas: List[Article_MetaData],
                             scrap_images: bool = True) -> List[Article]:
        """Scraps a batch of article from a given batch of URLs"""
        articles = []
        for item in metadatas:
            try:
                article = self.__fetch_article(item, scrap_images)
                articles.append(article)
            except Exception as e:
                pass

        return articles