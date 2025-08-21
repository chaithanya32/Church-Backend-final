# utilities/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql://postgres:chaithu@localhost/churchDB"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ Add this function:
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
