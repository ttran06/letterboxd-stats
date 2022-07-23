import scrapy
from scrapy.loader import ItemLoader
from letterboxd.items import MovieItem

import pandas as pd


class MoviesSpider(scrapy.Spider):
    name = "movies"

    allowed_domains = ["letterboxd.com"]
    start_urls = ["https://letterboxd.com/film/"]
    BASE_URL = "https://letterboxd.com"

    custom_settings = {"DEPTH_LIMIT": 1}

    def __init__(self, diary_file="letterboxd/spiders/diary.csv", *args, **kwargs):
        super(MoviesSpider, self).__init__(*args, **kwargs)
        self.diary = pd.read_csv(diary_file)
        self.diary.drop_duplicates(subset=["Name", "Year"], inplace=True)
        self.diary["Date"] = pd.to_datetime(self.diary["Date"])
        self.diary["Watched Date"] = pd.to_datetime(self.diary["Watched Date"])
        self.start_urls = self.diary["Letterboxd URI"].tolist()

    def parse(self, response):
        movie_url = response.url.replace("ttran06/", "")
        yield response.follow(movie_url, callback=self.parse_movies)

    def parse_movies(self, response):
        loader = ItemLoader(item=MovieItem(), response=response)

        movie_title = response.css("h1.headline-1::text").get()
        loader.add_css("title", "h1.headline-1::text")
        loader.add_css("director", 'div#tab-crew a[href^="/director"]::text')
        loader.add_css("actors", "div.cast-list p a::text")
        loader.add_css("actors_link", 'div.cast-list p a::attr("href")')
        loader.add_css("genres", 'div#tab-genres a[href^="/films/genre"]::text')
        loader.add_css("rating", 'head > meta[name="twitter:data2"]::attr(content)')
        loader.add_css("country", 'div#tab-details a[href^="/films/country"]::text')
        loader.add_css("production_company", 'div#tab-details a[href^="/studio"]::text')
        loader.add_css("release_year", 'a[href^="/films/year"]::text')
        loader.add_value(
            "watched_on",
            len(self.diary.loc[self.diary["Name"] == movie_title, "Watched Date"]),
        )
        loader.add_value(
            "user_rating",
            self.diary.loc[self.diary["Name"] == movie_title, "Rating"].tolist(),
        )

        yield loader.load_item()
