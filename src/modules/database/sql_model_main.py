from sqlmodel import create_engine, Session

from credentials import database_url_local


def get_session():
    engine = create_engine(database_url_local)
    with Session(engine) as session:
        yield session
