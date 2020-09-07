import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = os.environ['DATABASE_URL']

if db_url.startswith("sqlite"):
    engine = create_engine(
        db_url, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        db_url
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()