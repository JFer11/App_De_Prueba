from flask import Blueprint, request, jsonify, g

from training.controllers.function_decorators import login_required
from training.extensions import db
from training.models.articles import Article
from training.models.users import User

bp = Blueprint('article', __name__, url_prefix='/articles')

"""user = User(id='Fernando', username='Fernando', password='Fernando', email='fernando@g.com')
db.session.add(user)
db.session.commit()

article = Article(title="titulo new", body="El cuerpo papa", author=user)
db.session.add(article)
db.session.commit()"""


@login_required
@bp.route('/register', methods=['POST'])
def create_article():
    if not request.json or "title" not in request.json or "body" not in request.json:
        return jsonify({'Error': 'Bad request, "title" and "body" is required!'}), 400

    if len(request.json['title']) > 50 or len(request.json['body']) > 1000:
        return jsonify({'Error': 'Bad request, max length for "title" is 50 and max length for "body" is 1000.'}), 400

    article = Article(title=request.json['title'], body=request.json['body'], author=g.user)
    db.session.add(article)
    db.session.commit()
    db.session.refresh(article)

    # Later, we are going to serialize article w marshmallow.
    return jsonify({
        'Detail': 'Article created successfully',
        'Article': {
            'title': article.title,
            'body': article.body,
            'user_id': article.user_id
        }
    }), 200


# Hay que serializr esto
@login_required
@bp.route('/list', methods=['GET'])
def list_articles():
    articles = Article.query.filter_by(user_id=g.user.id).all()
    for article in articles:
        print(article.title)
    return "Bien"