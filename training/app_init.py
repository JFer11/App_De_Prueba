from flask import Flask
from flask_bcrypt import Bcrypt
from training.main import init_db

app = Flask(__name__)
from training.controllers.all_controllers import *
bcrypt = Bcrypt(app)

def main():
    init_db()
    app.run(port=8000, debug=True)


if __name__ == '__main__':
    main()
