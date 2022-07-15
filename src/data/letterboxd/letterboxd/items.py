# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re

import scrapy
from scrapy.loader.processors import MapCompose


def get_rating(text):
    rating_re = re.compile("(\d\.\d{2}) out of 5")
    rating = float(re.search(rating_re, text).group(1))

    return rating


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    genres = scrapy.Field()
    rating = scrapy.Field(input_processor=MapCompose(get_rating))
    country = scrapy.Field()
    production_company = scrapy.Field()
    release_year = scrapy.Field()
