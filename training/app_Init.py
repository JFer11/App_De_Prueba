from flask import Flask
from training.main import init_db
app = Flask(__name__)
from training.controllers.allControllers import *


def main():
    init_db()
    app.run(port=8000, debug=True)


if __name__ == '__main__':
    main()
