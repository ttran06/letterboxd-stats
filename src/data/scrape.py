import re

import requests
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup


def get_director(movie_soup):
    directors = movie_soup.select('div#tab-crew a[href^="/director"]')
    director_list = [director.text for director in directors]

    return director_list


def get_cast(movie_soup):
    casts = movie_soup.select("div.cast-list p a")
    cast_list = [cast.text for cast in casts]

    return cast_list


def get_genres(movie_soup):
    genres = movie_soup.select('div#tab-genres a[href^="/films/genre"]')
    genre_list = [genre.text for genre in genres]

    return genre_list


def get_rating(movie_soup):
    rating_re = re.compile("(\d\.\d{2}) out of 5")
    r = movie_soup.find("meta", attrs={"name": "twitter:data2"})["content"]
    rating = float(re.search(rating_re, r).group(1))

    return rating


def get_country(movie_soup):
    countries = movie_soup.select('div#tab-details a[href^="/films/country"]')
    country_list = [country.text for country in countries]

    return country_list


def get_production_company(movie_soup):
    studios = movie_soup.select('div#tab-details a[href^="/studio"]')
    studio_list = [studio.text for studio in studios]

    return studio_list


def get_release_year(movie_soup):
    year = movie_soup.select('a[href^="/films/year"]')

    return int(year[0].text)


def get_title(movie_soup):
    title = movie_soup.select("h1.headline-1")[0].text

    return title


def _getMovieUrl(url):
    f = urllib.request.urlopen(url)
    full_url = f.geturl()

    return full_url.replace("ttran06/", "")


def _finalizeDF(df):
    """
    make primary key column
    """
    df = df.explode(df.columns[-1])

    df["index"] = df[df.columns[-1]].factorize()[0]

    df = df.set_index("index")

    return df


def scrape(diary_path):
    diary = pd.read_csv(diary_path)
    diary.loc[:, "Movie URL"] = diary.apply(
        lambda x: _getMovieUrl(x["Letterboxd URI"]), axis=1
    )
    diary.to_csv("diary-links.csv", index=False)
    movie_urls = diary["Movie URL"].to_list()

    movie = pd.DataFrame(
        columns=["title", "year", "rating", "user_rating", "num_watch"]
    )
    director = pd.DataFrame(columns=["movie_id", "name"])
    actor = pd.DataFrame(columns=["movie_id", "name"])
    production_company = pd.DataFrame(columns=["movie_id", "name"])
    country = pd.DataFrame(columns=["movie_id", "country"])
    genre = pd.DataFrame(columns=["movie_id", "genre"])

    for movie_url in movie_urls:
        response = requests.get(movie_url)

        if response.status_code != 404:
            soup = BeautifulSoup(response.content, "lxml")

            num_watch = len(
                diary[
                    (diary["Name"] == get_title(soup))
                    & (diary["Year"] == get_release_year(soup))
                ]
            )
            user_avg_rating = diary[
                (diary["Name"] == get_title(soup))
                & (diary["Year"] == get_release_year(soup))
            ]["Rating"].mean()

            movie.loc[len(movie)] = [
                get_title(soup),
                get_release_year(soup),
                get_rating(soup),
                user_avg_rating,
                num_watch,
            ]
            director.loc[len(director)] = [len(movie) - 1, get_director(soup)]
            actor.loc[len(actor)] = [len(movie) - 1, get_cast(soup)]
            production_company.loc[len(production_company)] = [
                len(movie) - 1,
                get_production_company(soup),
            ]
            country.loc[len(country)] = [len(movie) - 1, get_country(soup)]
            genre.loc[len(genre)] = [len(movie) - 1, get_genres(soup)]

    director = _finalizeDF(director)
    actor = _finalizeDF(actor)
    production_company = _finalizeDF(production_company)
    country = _finalizeDF(country)
    genre = _finalizeDF(genre)

    movie[["user_rating"]] = movie[["user_rating"]].fillna("9")

    movie.to_csv("data/movie.csv", index_label="index")
    director.to_csv("data/director.csv")
    actor.to_csv("data/actor.csv")
    production_company.to_csv("data/production_company.csv")
    country.to_csv("data/country.csv")
    genre.to_csv("data/genre.csv")


if __name__ == "__main__":
    scrape()
