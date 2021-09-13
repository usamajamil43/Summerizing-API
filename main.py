import nltk

from cbs import ContentPublishingSystem
from constants import *

nltk.download('punkt')

if __name__ == '__main__':

    cbs = ContentPublishingSystem(URLS, API_TOKEN, TEMPLATE_ID,
                                  SLIDE_TEMPLATE_ID, LAYER_TEMPLATE_ID,
                                  LAYER_TEMPLATE_ID, REPEAT_TIME, ENDPOINT,
                                  True)

    cbs.ignite()
