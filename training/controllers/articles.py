from flask import Blueprint, request, jsonify, g

from training.controllers.function_decorators import login_required
from training.extensions import db
from training.models.articles import Article, ArticleSchema
from training.models.users import User

bp = Blueprint('article', __name__, url_prefix='/articles')


@bp.route('/register', methods=['POST'])
@login_required
def create_article():
    if not request.json or "title" not in request.json or "body" not in request.json:
        return jsonify({'Error': 'Bad request, "title" and "body" is required!'}), 400

    if len(request.json['title']) > 50 or len(request.json['body']) > 1000:
        return jsonify({'Error': 'Bad request, max length for "title" is 50 and max length for "body" is 1000.'}), 400

    article = Article(title=request.json['title'], body=request.json['body'], author=g.user)
    db.session.add(article)
    db.session.commit()
    db.session.refresh(article)

    article_schema = ArticleSchema()
    output = article_schema.dump(article)

    return jsonify({
        'Detail': 'Article created successfully',
        'Article': output
    }), 200


def get_articles(user):
    order_by = request.headers.get('order_by_date', 'DESC')
    if order_by == "ASC":
        return Article.query.filter_by(user_id=user.id).order_by(Article.created_at.asc()).all()
    elif order_by == "DESC":
        return Article.query.filter_by(user_id=user.id).order_by(Article.created_at.desc()).all()
    else:
        return Article.query.filter_by(user_id=user.id).order_by(Article.created_at.desc()).all()


def get_user(username):
    if username is None:
        user = g.user
    else:
        user = User.query.filter_by(username=username).first()
    return user


@bp.route('/list', methods=['GET'])
@bp.route('/list/<username>', methods=['GET'])
@login_required
def list_articles(username=None):
    user = get_user(username)
    if user is None:
        return jsonify({'Detail': 'Bad URL, "user" not found.'}), 404

    MAX_LIMIT = 20
    response = {
        'Detail': 'List of articles.'
    }

    if not request.args:
        articles_list = get_articles(user)
        response['Total articles'] = len(articles_list)
    else:
        # We get the parameters
        try:
            start = request.args.get('start', default=1, type=int)
            limit = request.args.get('limit', default=MAX_LIMIT, type=int)
        except ValueError:
            return jsonify({'Detail': 'Bad URL, check your URL parameters.'}), 400

        # We get all articles from logged user.
        articles_list_all = get_articles(user)

        # We validate parameters.
        length = len(articles_list_all)

        if start < 1 or limit < 1:
            return jsonify({'Detail': 'Bad URL, check your URL parameters (Negative or Zero values).'}), 400
        if start > length:
            return jsonify({'Detail': 'Bad URL, check your URL parameters (Start parameter number is too large).'}), 400
        if limit > MAX_LIMIT:
            return jsonify({'Detail': f'Bad URL, check your URL parameters (Limit parameter number is too large, '
                                      f'Max Limit={MAX_LIMIT}).'}), 400

        # We get the sublist of articles based on the parameters.
        end = start - 1 + limit
        if length < start-1+limit:
            end = length

        articles_list = articles_list_all[start-1:end]

        # We add interesting information about the original request to the response body.
        response['Total articles'] = length
        response['Start parameter'] = start
        response['Limit parameter'] = limit

    # We add to the response body the items that were selected.
    article_schema = ArticleSchema()
    for article in articles_list:
        article_schema.dump(article)
        if 'Articles' in response:
            output = article_schema.dump(article)
            response['Articles'].append(output)
        else:
            output = article_schema.dump(article)
            response['Articles'] = [output]

    return jsonify(response), 200
