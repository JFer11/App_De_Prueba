from datetime import datetime
from training.extensions import db


class Article(db.Model):
	__tablename__ = 'articles'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False, unique=True)
	body = db.Column(db.String(1000), nullable=False)
	path_to_image = db.Column(db.String(50), unique=True)
	created_at = db.Column(db.DateTime(), default=datetime.now())
	# db.ForeignKey('users.id') because here we reference the table name
	user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)

	def __str__(self):
		return self.id
