from typing import Sequence
import config
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


Base = declarative_base()


class Movie(Base):
    """
    class for the Movie database
    """

    __tablename__ = "movies"
    id = Column(Integer, Sequence(), primary_key=True)


def save_in_db(data, table_name):
    # connect to server
    engine = create_engine(
        f"mysql://{config.username}:{config.password}@{config.host}/{config.dbname}",
        echo=True,
    )
    # if not database_exists(engine.url):
    # create_database(engine.url)


#
# conn = engine.connect()

# TODO: create tables
# movie table
# actor table
# country table
# director table
# genre table
# movieactor ta ble
# moviecountry table
# moviedirector
# moviegenre
