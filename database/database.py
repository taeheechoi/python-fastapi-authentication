from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLITE_DATABASE_URL = 'sqlite:///./database.db'

engine = create_engine(SQLITE_DATABASE_URL, echo=True, connect_args={'check_same_thread': False})
# echo=True argument enables logging of SQL statements, while connect_args={“check_same_thread”: False} allows SQLite to work with multiple threads.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 
# base class will be used to define models

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()