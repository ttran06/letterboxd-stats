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
        loader = ItemLoader(item=MovieItem(), response=response)

        movie_title = response.css("h1.headline-1::text").get()
        casts = response.css("div.cast-list p a::text").extract()
        loader.add_css("title", response.css("h1.headline-1::text").get())
        loader.add_css("director", response.css('div#tab-crew a[href^="/director"]::text').extract())
        loader.add_css("casts", response.css("div.cast-list p a::text").extract())
        loader.add_css('casts_link', response.css('div.cast-list p a::attr("href")').extract())
        loader.add_css('genres', response.css('div#tab-genres a[href^="/films/genre"]::text').extract())
        loader.add_css('rating',
            response.css('head > meta[name="twitter:data2"]::attr(content)').get()
        )
        loader.add_css('country', response.css(
            'div#tab-details a[href^="/films/country"]::text'
        ).extract())
        loader.add_css('production_company', response.css(
            'div#tab-details a[href^="/studio"]::text'
        ).extract())
        loader.add_css('release_year', response.css('a[href^="/films/year"]::text').get())
        loader.add_value('count', self.calculated_diary.loc[
            self.calculated_diary["Name"] == movie_title, "Rating"
        ].iloc[0, 0])
        loader.add_value('mean', self.calculated_diary.loc[
            self.calculated_diary["Name"] == movie_title, "Rating"
        ].iloc[0, 1])

        yield loader.load_item()

