from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Application(Flask):
    def __init__(self,import_name):
        super(Application,self).__init__(import_name)


app = Flask(Flask)
db = SQLAlchemy(app)