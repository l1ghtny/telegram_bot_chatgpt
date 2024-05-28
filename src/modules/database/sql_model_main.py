from sqlmodel import create_engine, Session

from credentials import database_url_local

engine = create_engine(database_url_local)


def get_session():
    with Session(engine) as session:
        yield session
