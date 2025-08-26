from flask import Flask
from flask_smorest import Api


from config import BaseConfig
from api.api import blueprint
app = Flask(__name__)
app.config.from_object(BaseConfig)# we use from_object method to load configuration from a class
#loads all the configuration options from our config.py
kitchen_api = Api(app)# we create the instance of flask_smorest's Api object

kitchen_api.register_blueprint(blueprint)