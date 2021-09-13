"""This script puts it all together. It scraps news articles links from the provided XML sources. 
It then scraps those links for article text and images, genereates appropriate json objects and send the over HTTP to 
specified API end-point. This whole process repeats after every REPEAT_TIME minutes.
"""

from time import sleep
from typing import List

import requests

from article import Article, Article_MetaData
from article_scrapper import ArticleScrapper
from log import log_error, log_info
from rss_scraper import RssScraper
from story import Story


class ContentPublishingSystem:
    def __init__(self,
                 source: List[str],
                 api_token: str,
                 template_id: str,
                 slide_temp: str,
                 text_layer_temp: str,
                 image_layer_temp: str,
                 repeat_time: int,
                 api_endpoint: str,
                 logging: bool = True) -> None:

        self.xml_sources = source
        self.api_token = api_token
        self.template_id = template_id
        self.slide_temp = slide_temp
        self.text_layer_temp = text_layer_temp
        self.image_layer_temp = image_layer_temp
        self.repeat_time = repeat_time
        self.logging = logging
        self.api_endpoint = api_endpoint
        self.articles_repo = set()
        self.headers = {'content-type': 'application/json'}

    def __fetch_raw_content(self) -> List[Article_MetaData]:
        """Scraps XML links for article links. Updates the repository of links
        that have been posted. Only returns newer articles.
        """
        rss_scraper = RssScraper()
        raw_info = set(rss_scraper.scrap_articles_links(self.xml_sources))

        latest = raw_info.difference(self.articles_repo)
        self.articles_repo.union(latest)

        if self.logging:
            log_info(f'Articles Links Scrapped: {len(latest)}')
        return list(latest)

    def __fetch_story_content(self) -> List[Article]:
        """Fetches articles text, image links and dimensions."""
        raw_data = self.__fetch_raw_content()
        article_scrapper = ArticleScrapper()
        articles = article_scrapper.fetch_articles_batch(raw_data, True)
        if self.logging:
            log_info(f'Articles Obtained: {len(articles)}')
        return articles

    def __make_stories(self) -> List[Story]:
        """Create story objects from raw article data."""
        articles = self.__fetch_story_content()
        stories = []
        for article in articles:
            story = Story(article)
            stories.append(
                story.make_story(template_id=self.template_id,
                                 slide_temp_id=self.slide_temp,
                                 api_key=self.api_token,
                                 text_layer_temp_id=self.text_layer_temp,
                                 image_layer_temp_id=self.image_layer_temp))
        if self.logging:
            log_info(f'Stories Created: {len(stories)}')
        return stories

    def publish_stories(self):
        """Publishes stories on the specifed API ENDPOINT"""
        stories = self.__make_stories()
        for story in stories:
            res = requests.post(self.api_endpoint,
                                data=story.json(),
                                headers=self.headers)
            if self.logging:
                if res.status_code == 200:
                    log_info(
                        f'Successfully posted story from: {story.article.meta.url}'
                    )

                else:
                    log_error(
                        f'Failed to post story from: {story.article.meta.url}')
                    # log_error(f'JSON: {story.json()}')
                    log_error(f'RESPONSE CODE: {res.status_code}')
                    # log_error(f'REASON: {res.text}')

    def ignite(self):
        """Starts the process"""
        minutes = 0
        while True:
            self.publish_stories()
            sleep(self.repeat_time * 60)
            minutes += self.repeat_time
            if minutes > 180:  # After every 3 hours
                self.articles_repo.clear()
                minutes = 0
