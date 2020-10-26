from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/baseparaflask')
Session = sessionmaker(engine)
session = Session()

def init_db():
    from training.models import users
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
