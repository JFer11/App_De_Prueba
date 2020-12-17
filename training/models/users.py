from datetime import datetime
from training.extensions import db, marshmallow
from marshmallow import fields, validate


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.String(50), primary_key=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(1000), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	mail_validation = db.Column(db.Boolean, unique=False, default=False)
	created_at = db.Column(db.DateTime(), default=datetime.now())
	path_to_image = db.Column(db.String(50), unique=True)

	def __str__(self):
		return self.username


class UserSchema(marshmallow.SQLAlchemySchema):
	"""This class is necessary for marshmallow. Marshmallow is used for serialization."""
	class Meta:
		model = User

	# Here we specify which fields we want to serialize
	# We want to ignore password, so its filed was not included below
	id = marshmallow.auto_field()
	username = marshmallow.auto_field()
	email = marshmallow.auto_field()
	mail_validation = marshmallow.auto_field()
	created_at = marshmallow.auto_field()


class UserSchemaValidationSignIn(marshmallow.SQLAlchemySchema):
	"""Here we validate important fields to login a User."""
	class Meta:
		model = User

	# Here we specify which fields we want to serialize
	# We want to ignore password, so its filed was not included below
	username = fields.Str(validate=validate.Length(min=1, max=50), required=True)
	password = fields.Str(validate=validate.Length(min=1, max=50), required=True)


class UserSchemaValidationSignUp(UserSchemaValidationSignIn):
	"""Here we validate important fields to register a User."""

	# Here we need to validate the same fields as the login view function and also its email.
	email = fields.Email(required=True)
