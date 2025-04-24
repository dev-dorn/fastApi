from flask import Flask
from flask_smorest import Api
from config import BaseConfig
from api.api import blueprint

app = Flask(__name__)
app.config.from_object(BaseConfig)

api = Api(app)
api.register_blueprint(blueprint)

@app.route('/')
def index():
    return 'Welcome to the Kitchen API. Visit /docs for Swagger UI or /redoc for ReDoc.'
