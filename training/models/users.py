from datetime import datetime
from training.extensions import db


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.String(50), primary_key=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(1000), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	mail_validation = db.Column(db.Boolean, unique=False, default=False)
	created_at = db.Column(db.DateTime(), default=datetime.now())

	def __str__(self):
		return self.username