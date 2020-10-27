from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from training import main


class User(main.Base):
	__tablename__ = 'users'
	id = Column(String(50), primary_key=True)
	username = Column(String(50), nullable=False, unique=True)
	password = Column(String(1000), nullable=False)
	email = Column(String(50), nullable=False, unique=True)
	mail_validation = Column(Boolean, unique=False, default=False)
	created_at = Column(DateTime(), default=datetime.now())

	def __str__(self):
		return self.username
