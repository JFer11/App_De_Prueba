from datetime import datetime
from training.extensions import db, marshmallow
from marshmallow import fields, validate


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


class ArticleSchema(marshmallow.SQLAlchemySchema):
	"""This class is necessary for marshmallow. Marshmallow is used for serialization."""
	class Meta:
		model = Article

	# Here we specify which fields we want to serialize.
	# We want to ignore path_to_image, so its filed was not included below
	id = marshmallow.auto_field()
	title = marshmallow.auto_field()
	body = marshmallow.auto_field()
	created_at = marshmallow.auto_field()
	user_id = marshmallow.auto_field()


class ArticleSchemaValidation(marshmallow.SQLAlchemySchema):
	"""Here we validate important fields to create an Article."""
	class Meta:
		model = Article

	# Here we specify which fields we want to validate.
	title = fields.Str(validate=validate.Length(min=1, max=50), required=True)
	body = fields.Str(validate=validate.Length(min=1, max=1000), required=True)
