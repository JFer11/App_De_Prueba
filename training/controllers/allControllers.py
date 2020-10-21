from training.appInit import app
from flask import render_template
from flask import request
from training.controllers import indexForm, loginForm
from flask import abort, redirect, url_for
from training.main import session

from training.models.users import User


@app.route('/')
def primera():
	return "HOLAAAA"


@app.route('/index', methods=['GET', 'POST'])
def signup():
	form = indexForm.RegistrationForm(request.form)

	if request.method == 'POST':
		if form.validate():
			#Guardar en la base
			id = request.form['username']
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			user = User(id=id,username=username,email=email,password=password)

			session.add(user)
			session.commit()

			#Redireccionar a otro HTML que entre a la pagina
			return redirect(url_for('sign_in'))
		else:
			form = indexForm.RegistrationForm()
			return render_template('index.html',form=form,alert=True)

	return render_template('index.html', form=form, alert=False)


@app.route('/login', methods=['GET', 'POST'])
def sign_in():
	form = loginForm.loginWTForm(request.form)

	if request.method == 'POST' and form.validate():
		our_user = session.query(User).filter_by(id=request.form['username']).first()

		if not isinstance(our_user,type(None)):
			#Si lo encontre en la base, me meto aca

			#Chequea el password a ver si coincide
			if our_user.password == request.form['password']:
				return redirect(url_for('inside'))
			return render_template('login.html', form=form, alert=True)

		else:
			return render_template('login.html', form=form, alert=True)


	return render_template('login.html',form=form)

@app.route('/inside')
def inside():
	return "Adentrooooo"


