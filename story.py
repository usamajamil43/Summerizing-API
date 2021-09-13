"""This script implements the functionality to create a story consisting of multiple slides 
out of an article object. As the story would be sent over the network, therefore json 
serialization will be used
"""

from __future__ import annotations
from itertools import zip_longest
from typing import Optional
import json

from nltk import sent_tokenize

from article import Article
from article import Image


class Story:
    def __init__(self, article: Article) -> None:
        self.article = article
        self.story = {}

    def __create_text_layer(self, layer_template_id: int, text: str) -> dict:
        return {"LayerTemplateId": layer_template_id, "Text": text}

    def __create_image_layer(
        self,
        layer_template_id: int,
        image: Image,
    ) -> dict:
        return {
            'LayerTemplateId': layer_template_id,
            'Image': {
                'Url': image.url,
                'Width': image.dimensions[0],
                'Height': image.dimensions[1]
            }
        }

    def __create_slide(self,
                       slide_template_id: int,
                       text_template_id: Optional[int] = None,
                       text: Optional[str] = None,
                       image_template_id: Optional[int] = None,
                       image: Optional[Image] = None):
        return {
            'SlideTemplateId':
            slide_template_id,
            'Layers':
            list(
                filter(lambda x: x, [
                    self.__create_text_layer(text_template_id, text)
                    if text else None,
                    self.__create_image_layer(image_template_id, image)
                    if image else None
                ]))
        }

    def __make_slides(self,
                      slide_temp_id: int,
                      text_layer_temp_id: Optional[int] = None,
                      image_layer_temp_id: Optional[int] = None):
        slides = []
        sentences = sent_tokenize(self.article.summary)
        images = self.article.images
        images = images[:len(sentences)]
        for sen, im in zip_longest(sentences, images):
            slides.append(
                self.__create_slide(slide_temp_id, text_layer_temp_id, sen,
                                    image_layer_temp_id, im))

        return slides

    def make_story(self,
                   template_id: int,
                   slide_temp_id: int,
                   api_key: str,
                   text_layer_temp_id: Optional[int] = None,
                   image_layer_temp_id: Optional[int] = None) -> Story:
        self.story = {
            'Title':
            self.article.meta.title,
            'Text':
            self.article.meta.title,
            'TemplateId':
            template_id,
            'APIKey':
            api_key,
            'Slides':
            self.__make_slides(slide_temp_id, text_layer_temp_id,
                               image_layer_temp_id)
        }
        return self

    def json(self) -> str:
        return json.dumps(self.story)
