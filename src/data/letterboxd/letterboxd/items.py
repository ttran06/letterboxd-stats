# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Field, Item
from scrapy.loader.processors import MapCompose, TakeFirst


def get_rating(text):
    rating = float(text.split()[0])

    return rating


def filter_casts(text):
    # "Show All…"
    return None if "Show All" in text else text


def make_float(x):
    return float(x)


class MovieItem(Item):
    # define the fields for your item here like:
    title = Field(output_processor=TakeFirst())
    director = Field()
    actors = Field(input_processor=MapCompose(filter_casts))
    actors_link = Field()
    genres = Field()
    rating = Field(
        input_processor=MapCompose(get_rating, make_float), output_processor=TakeFirst()
    )
    country = Field()
    production_company = Field()
    release_year = Field(input_process=MapCompose(int), output_processor=TakeFirst())
    watched_on = Field()
    user_rating = Field()
