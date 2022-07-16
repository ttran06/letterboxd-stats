# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Field, Item
from scrapy.loader.processors import MapCompose


def get_rating(text):
    rating = float(text.split()[0])

    return rating


def filter_casts(text):
    return None if text == "Show All…" else text


def make_float(x):
    return float(x)


class MovieItem(Item):
    # define the fields for your item here like:
    title = Field()
    director = Field()
    actors = Field()
    actors_link = Field()
    genres = Field()
    rating = Field(input_processor=MapCompose(get_rating, make_float))
    country = Field()
    production_company = Field()
    release_year = Field(input_process=MapCompose(int))
    count = Field()
    mean = Field()
