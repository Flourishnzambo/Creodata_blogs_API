import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

from psycopg2.extras import RealDictCursor
import time

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

# connecting to database
while True:

    try:
       conn = psycopg2.connect(host= 'localhost',database='blogdb', user='postgres', password='39901121' , cursor_factory=RealDictCursor )
       cursor = conn.cursor()
       print("Database connection was succcessful!")
       break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)

#  Create tables from models
if __name__ == "__main__":
    from app import models
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
