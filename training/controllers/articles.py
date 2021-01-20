from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError

from training.controllers.function_decorators import login_required
from training.extensions import db
from training.models.articles import Article, ArticleSchema, ArticleSchemaValidation
from training.models.users import User

bp = Blueprint('article', __name__, url_prefix='/articles')


def validate_article(request_json):
    try:
        ArticleSchemaValidation().load(request_json)
        return {
            "Valid": True,
            "Details": "All fields are valid."
        }
    except ValidationError as err:
        return {
            "Valid": False,
            "Details": [err.messages, err.valid_data]
        }


@bp.route('/register', methods=['POST'])
@login_required
def create_article():
    valid = validate_article(request.json)
    if valid['Valid'] is False:
        return jsonify({'Error': valid['Details']}), 400

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


def get_queryset_asc_or_desc_articles(user):
    order_by = request.headers.get('order_by_date', 'DESC')
    if order_by == "ASC":
        return Article.query.filter_by(user_id=user.id).order_by(Article.created_at.asc())
    elif order_by == "DESC":
        return Article.query.filter_by(user_id=user.id).order_by(Article.created_at.desc())
    else:
        return Article.query.filter_by(user_id=user.id).order_by(Article.created_at.desc())


def get_user(username):
    if username is None:
        user = g.user
    else:
        user = User.query.filter_by(username=username).first()
    return user


def paginated_articles(schema_class, limit, offset, queryset):
    if limit is None:
        raw_articles_list = queryset.offset(offset).all()
    else:
        raw_articles_list = queryset.offset(offset).limit(limit).all()

    article_schema = schema_class()  # Here, will be ArticleSchema()
    result = list(map(lambda article: article_schema.dump(article), raw_articles_list))

    """
    Classical solution:
    
    result = []

    article_schema = schema_class()  # Here, will be ArticleSchema()
    for article in raw_articles_list:
        result.append(article_schema.dump(article))
    """

    return result


def get_offset_articles():
    try:
        offset = request.args.get('offset', default=0, type=int)
    except ValueError:
        return jsonify({'Detail': 'Bad URL, check your URL parameters.'}), 400

    if offset < 0:
        return 0
    return offset


def get_limit_articles():
    MAX_LIMIT = 20
    try:
        limit = request.args.get('limit', default=MAX_LIMIT, type=int)
    except ValueError:
        return jsonify({'Detail': 'Bad URL, check your URL parameters.'}), 400

    if limit < 0:
        return None

    if limit > MAX_LIMIT:
        return jsonify({'Detail': f'Bad URL, check your URL parameters (Limit parameter number is too large, '
                                  f'Max Limit={MAX_LIMIT}).'}), 400
    return limit


def get_count_articles(user):
    return Article.query.filter_by(user_id=user.id).count()


@bp.route('/list', methods=['GET'])
@bp.route('/list/<username>', methods=['GET'])
@login_required
def list_articles(username=None):
    user = get_user(username)
    if user is None:
        return jsonify({'Detail': 'Bad URL, "user" not found.'}), 404

    queryset = get_queryset_asc_or_desc_articles(user)
    offset = get_offset_articles()
    limit = get_limit_articles()
    count = get_count_articles(user)
    result = paginated_articles(ArticleSchema, limit, offset, queryset)

    response = {'Detail': 'List of articles.', 'Total articles': count, 'Offset parameter': offset,
                'Limit parameter': limit, 'Result': result}

    # if offset > count: no article will be displayed
    return jsonify(response), 200
