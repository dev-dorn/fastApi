from flask import Flask
from flask_smorest import Api
from config import BaseConfig
from api.api import blueprint
from pathlib import Path

import yaml
from apispec import APISpec
app = Flask(__name__)
app.config.from_object(BaseConfig)

api = Api(app)
api.register_blueprint(blueprint)

api_spec = yaml.safe_load((Path(__file__).parent / "oas.yaml").read_text())
spec = APISpec(
    title=api_spec["info"]["title"],
    version=api_spec["info"]["version"],
    openapi_version=api_spec["openapi"]
    )
spec.to_dict = lambda: api_spec
api.spec = spec

@app.route('/')
def index():
    return 'Welcome to the Kitchen APi. Visit /docs for Swagger UI or /redoc for ReDoc.'
