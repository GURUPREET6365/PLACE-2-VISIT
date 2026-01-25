from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


engine = create_engine(os.getenv('DATABASE_URL'))
sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
"""
This Base is the identifier for the class that will converted into tables. This contains orm and other details to change the columns property into constraints.
"""



# This creates the connection on each request and yield stop till the execution. This is called dependency.
def get_db():
    db=sessionLocal()

    try:
        yield db

    finally:
        db.close()