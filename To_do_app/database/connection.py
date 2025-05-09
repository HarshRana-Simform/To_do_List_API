from pydantic_core import MultiHostUrl
from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv, get_key

load_dotenv()


def SQLALCHEMY_DATABASE_URI() -> PostgresDsn:
    return MultiHostUrl.build(
        scheme="postgresql+psycopg",
        username=get_key(".env", "POSTGRES_USER"),
        password=get_key(".env", "POSTGRES_PASSWORD"),
        host=get_key(".env", "POSTGRES_SERVER"),
        port=int(get_key(".env", "POSTGRES_PORT")),
        path=get_key(".env", "POSTGRES_DB"),
    )


engine = create_engine(str(SQLALCHEMY_DATABASE_URI()), echo=True)

Sessionlocal = Session(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Sessionlocal
    try:
        yield db
    finally:
        db.close()
