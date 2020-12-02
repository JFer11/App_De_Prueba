from flask import Blueprint, request, redirect, render_template, url_for, g, current_app, flash, make_response, \
    jsonify, abort
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os

from training.extensions import db
from training.controllers.function_decorators import login_required
from training.controllers.forms.upload_image_avatar_form import UploadImageForm


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('avatar', __name__, url_prefix='/user')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_path_to_database_user(path_to_image):
    if len(path_to_image) > 50:
        abort(400)
    else:
        if g.user.path_to_image is None:
            g.user.path_to_image = path_to_image
            db.session.commit()
        else:
            os.remove(f"uploads/{g.user.username}/{g.user.path_to_image}")
            g.user.path_to_image = path_to_image
            db.session.commit()


@bp.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Path too long, bad request.',
                                  "param": error}), 400)


def rename(filename):
    raw_email = str(g.user.email)
    a = raw_email + "_" + filename
    print(raw_email)
    print(filename)
    print(a)
    return a


def create_folder_if_not_exist(user_folder):
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], user_folder)
    if not os.path.exists(path):
        os.makedirs(path)


@bp.route('/modify/image', methods=['GET', 'POST'])
@login_required
def add_avatar_image():
    form = UploadImageForm(request.form)

    if request.method == 'POST':

        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return "No subiste ningun archivo"

        file = request.files.get('image')

        # if ruse does not select file, browser also
        # submit an empty part without filename.
        # However, frontend should not let submit if no file was uploaded. Because of validators.
        # This check is for the api.
        if file.filename == '':
            flash('No selected file')
            return render_template('modify_image.html', form=form, username=g.user, alert_no_file=True), 201

        if file and allowed_file(file.filename):
            # Inside here, "filename" is the file name to be stored
            filename = secure_filename(file.filename)
            user_folder = g.user.username
            create_folder_if_not_exist(user_folder)
            path_to_image = os.path.join(current_app.config['UPLOAD_FOLDER'], user_folder, filename)
            save_path_to_database_user(filename)
            file.save(path_to_image)

            # After saved the name of the file into the database, we proceed to display the recently uploaded image.
            return redirect(url_for('avatar.uploaded_file', filename=filename))

    return render_template('modify_image.html', form=form, username=g.user), 200


@bp.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    """The image is sent to the client as a response body"""

    path = os.path.join(current_app.config['UPLOAD_FOLDER'], g.user.username)

    # if we add the key word as_attachment=True, instead of showing the image. The browser will download it.
    return send_from_directory(path, filename)


@bp.route('/')
@login_required
def show_user():
    user = g.user
    return render_template('show_user.html', user=user), 200
