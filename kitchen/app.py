from flask import Flask
from flask_smorest import Api

from config import BaseConfig


app = Flask(__name__) # we create an instance of tthe flask application object
app.config.from_object(BaseConfig)
kitchen_api = Api(app) # we create an instance of flask-smorest's Api object