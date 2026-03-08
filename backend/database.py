from sqlalchemy import create_engine #bridge between python app and db
from sqlalchemy.orm import sessionmaker, declarative_base #creates db sessions to query or modify data

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"  # local SQLite file

engine = create_engine( #creates the actual engine
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} #allows multiple threads to access DB safely
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #SessionLocal = factory for creating DB sessions, autocommit = False: actively commit changes to save to db, autoflush = False: wont automatically push changes DB, bind=engine: binds the engine with the session
Base = declarative_base() #base class for all models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()