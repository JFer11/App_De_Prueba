#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
#import os


#Base = declarative_base()

#engine = None
#session = None
#Siempre se sustituyen por None, aunque las cambie abajo
#engine = create_engine(os.environ.get("DATABASE_URL"))
#Session = sessionmaker(engine)
#session = Session()


#def init_db():
    #global engine
    #global session
   # from training.models import users
    #Base.metadata.drop_all(engine)
#    Base.metadata.create_all(engine)
