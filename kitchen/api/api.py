import uuid
from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint

blueprint = Blueprint('kitchen', __name__, description='Kitchen API')

schedules = [{
    'id': str(uuid.uuid4()),
    'scheduled': datetime.now(),
    'status': 'pending',
    'order':[{
        'product': 'ca'
    }]
    
}]
