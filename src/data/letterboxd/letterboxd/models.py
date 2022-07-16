from . import config

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Table,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def db_connect():
    """
    Database connection using database settings from config.py

    Returns sqlalchemy engine instance
    """

    return create_engine(
        f"mysql://{config.username}:{config.password}@{config.host}/{config.dbname}",
        echo=True,
    )


def create_table(engine):
    # will not create table that already exists
    Base.metadata.create_all(engine, checkfirst=True)


# Association Table for Many-to-Many relationship between Movie and Genre
# one movie can have many tags, one tag can have many movies
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
movie_director = Table(
    "movie_director",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("director_id", Integer, ForeignKey("director.id")),
)
movie_actors = Table(
    "movie_actors",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("actor_id", Integer, ForeignKey("actor.id")),
)
movie_genre = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("genre_id", Integer, ForeignKey("genre.id")),
)
movie_country = Table(
    "movie_country",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("country_id", Integer, ForeignKey("country.id")),
)
movie_production_company = Table(
    "movie_production_company",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("production_company_id", Integer, ForeignKey("production_company.id")),
)


class Movie(Base):
    """
    class for the Movie database
    """

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column("title", String(150), nullable=False)
    # Many-to-Many relationship between movie and director
    director = relationship(
        "director", secondary="movie_director", lazy="dynamic", backref="movies"
    )
    actors = relationship(
        "actors", secondary="movie_actors", lazy="dynamic", backref="movies"
    )
    genres = relationship(
        "genres", secondary="movie_genres", lazy="dynamic", backref="movies"
    )
    rating = Column("rating", Float)
    user_rating = Column("user_rating", Float, nullable=True)
    country = relationship("country", secondary="movies_country")
    production_company = relationship(
        "production_company",
        secondary="movie_production_company",
        lazy="dynamic",
        backref="movie",
    )
    release_year = Column("release_year", Integer)
    num_watch = Column("num_watch", Integer)


class Director(Base):
    """
    class for the Director database
    """

    __tablename__ = "director"

    id = Column(Integer, primary_key=True)
    name = Column("name", String(50))
    movies = relationship(
        "movie", secondary="movies_director", lazy="dynamic", backref="director"
    )


class Actor(Base):
    """
    class for the Actor database
    """

    __tablename__ = "actor"

    id = Column(Integer, primary_key=True)
    name = Column("name", String(50))
    link = Column("link", String(200), unique=True)
    movies = relationship(
        "movie", secondary="movies_actors", lazy="dynamic", backref="actor"
    )


class Genre(Base):
    """
    class for Genre database
    """

    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    genre = Column("genre", String(30), unique=True)
    movies = relationship(
        "movie", secondary="movies_genres", lazy="dynamic", backref="genre"
    )


class ProductionCompany(Base):
    """
    class for Production Company database
    """

    __tablename__ = "production_company"

    id = Column(Integer, primary_key=True)
    production_company = Column("production_company", String(60), unique=True)
    movies = relationship(
        "movie",
        secondary="movies_production_company",
        lazy="dynamic",
        backref="production_company",
    )


class Country(Base):
    """
    class for Country databaase
    """

    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    country = Column("country", String(30), unique=True)
    movies = relationship(
        "movie", secondary="movies_country", lazy="dynamic", backref="country"
    )
