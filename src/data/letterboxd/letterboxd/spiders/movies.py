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
        # calculate number of watches and avg rating
        self.calculated_diary = self.diary.groupby(
            ["Name", "Year"], as_index=False
        ).agg({"Rating": ["count", "mean"]})
        self.diary.drop_duplicates(subset=["Name", "Year"], inplace=True)
        self.start_urls = self.diary["Letterboxd URI"].tolist()

    def parse(self, response):
        movie_url = response.url.replace("ttran06/", "")
        loader = ItemLoader(item=MovieItem, selector)
        yield response.follow(movie_url, callback=self.parse_movies)

    def parse_movies(self, response):
        movie_title = response.css("h1.headline-1::text").get()
        director = response.css('div#tab-crew a[href^="/director"]::text').extract()
        casts = response.css("div.cast-list p a::text").extract()
        casts_link = response.css('div.cast-list p a::attr("href")').extract()
        genres = response.css('div#tab-genres a[href^="/films/genre"]::text').extract()
        rating = float(
            response.css('head > meta[name="twitter:data2"]::attr(content)').get()
        )
        country = response.css(
            'div#tab-details a[href^="/films/country"]::text'
        ).extract()
        production_company = response.css(
            'div#tab-details a[href^="/studio"]::text'
        ).extract()
        release_year = response.css('a[href^="/films/year"]::text').get()
        count = self.calculated_diary.loc[
            self.calculated_diary["Name"] == movie_title, "Rating"
        ].iloc[0, 0]
        mean = self.calculated_diary.loc[
            self.calculated_diary["Name"] == movie_title, "Rating"
        ].iloc[0, 1]

        if "Show All…" in casts:
            casts.remove("Show All…")

        yield {
            "movie": movie_title,
            "director": director,
            "casts": casts,
            "casts_link": casts_link,
            "genres": genres,
            "rating": rating,
            "country": country,
            "production_company": production_company,
            "release_year": release_year,
            "num_watch": count,
            "avg_user_rating": mean,
        }
        # loader = ItemLoader(item=MovieItem(), selector=movie)
