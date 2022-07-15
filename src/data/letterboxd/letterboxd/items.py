# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Field, Item
from scrapy.loader.processors import MapCompose


def get_rating(text):
    rating = float(text.split()[0])

    return rating


class MovieItem(Item):
    # define the fields for your item here like:
    id = Field()
    title = Field()
    director = Field()
    actors = Field()
    genres = Field()
    rating = Field(input_processor=MapCompose(get_rating))
    country = Field()
    production_company = Field()
    release_year = Field()
    count = Field()
    mean = Field()
