from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))

if __name__ == '__main__':
    engine = create_engine('sqlite:///tomatoes.db')
    Base.metadata.bind = engine
    # Create Table if doesn't exist
    Base.metadata.create_all(checkfirst=True)
