from flask import Flask
from training.main import init_db


app = Flask(__name__)

#from controllers import allControllers

init_db()
#print(type(init_db))



from training.controllers.allControllers import *


def main():
	app.run(port=8000, debug=True)


if __name__ == '__main__':
	main()
