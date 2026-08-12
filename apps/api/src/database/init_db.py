from database.connection import engine

from models.base import Base


def init_database():

    Base.metadata.create_all(

        bind=engine
    )

    print(
        "Database initialized."
    )