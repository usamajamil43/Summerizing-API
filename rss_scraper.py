"""Implements functionality to scrap RSS urls for news articles"""

from typing import List, Optional

from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests

from article import Article_MetaData


class RssScraper:
    def __fetch_rss_page(self, url: str) -> Optional[BeautifulSoup]:
        """fetches rss webpage"""
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, features='xml')
            return soup
        except Exception as e:
            print(e)
            return None

    def scrap_articles_links(self, urls: List[str]) -> List[Article_MetaData]:
        """Crawls the RSS webpage to scrap links contained inside item tags"""
        metadatas = []

        for url in urls:
            soup = self.__fetch_rss_page(url)
            if soup:
                articles_urls = soup.find_all('item')

                for item in articles_urls:
                    title = item.find('title').text
                    link = item.find('link').text
                    if link.count('://') == 0:
                        link = link.replace(':/', '://').strip()
                    date = item.find('pubDate').text.strip()
                    date = parse(date)
                    metadatas.append(Article_MetaData(title, link, date))

        return metadatas