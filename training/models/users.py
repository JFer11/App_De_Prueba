from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from training import main

#from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()


class User(main.Base):
	__tablename__ = 'users'
	id = Column(String(50), primary_key=True)
	username = Column(String(50), nullable=False, unique=True)
	password = Column(String(50),nullable=False)
	email = Column(String(50),nullable=False, unique=True)
	created_at = Column(DateTime(), default=datetime.now())

	def __str__(self):
		return self.username

