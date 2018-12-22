from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Application(Flask):
    pass


app = Flask(Flask)
db = SQLAlchemy(app)