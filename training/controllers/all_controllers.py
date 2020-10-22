from training.app_init import app
from flask import render_template
from flask import request
from training.controllers import index_form, login_form
from flask import redirect, url_for
from training.main import session
from flask import session as sesion
from training.models.users import User
from training.app_init import bcrypt
from markupsafe import escape
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def primera():
    return "HOLAAAA"


@app.route('/index', methods=['GET', 'POST'])
def signup():
    form = index_form.RegistrationForm(request.form)

    if request.method == 'POST':
        if form.validate():
            # Guardar en la base
            id = request.form['username']
            username = request.form['username']
            password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            #.decode('utf-8') Esto es muy raro, lo vi en un comentario de una respuesta de stack overflow
            # me parece que es porque en versiones anteoriores de bcrypt no hay
            email = request.form['email']
            user = User(id=id, username=username, email=email, password=password)

            session.add(user)
            session.commit()

            # Redireccionar a otro HTML que entre a la pagina
            return redirect(url_for('sign_in'))
        else:
            form = index_form.RegistrationForm(request.form)
            return render_template('index.html', form=form, alert=True)

    return render_template('index.html', form=form, alert=False)


@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    form = login_form.LoginWTForm(request.form)

    if request.method == 'POST' and form.validate():
        our_user = session.query(User).filter_by(id=request.form['username']).first()

        if our_user is not None:
            # Si lo encontre en la base, me meto aca

            # Chequea el password a ver si coincide
            if bcrypt.check_password_hash(our_user.password, request.form['password']):
                # Se le da la cookie session
                sesion['username'] = request.form['username']
                return redirect(url_for('inside'))
            return render_template('login.html', form=form, alert=True)

        else:
            return render_template('login.html', form=form, alert=True)

    return render_template('login.html', form=form)


@app.route('/inside')
def inside():
    if 'username' in sesion:
        return "Ya estas registrado como --> " + str(sesion['username'])

    return "No estas registrado"


@app.route('/logout')
def logout():
    if 'username' in sesion:
        a = sesion['username']
        sesion.pop('username', None)
        return "Se deslogueo la sesion. --> " + str(a)
    return "No habia sesiones iniciadas"


@app.route('/ver')
def ver():
    return sesion.get('username')