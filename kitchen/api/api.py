import uuid
from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint

from api.schema import (
    GetScheduledOrderSchema,
    ScheduleOrderSchema,
    GetScheduledOrdersSchema,
    SchedulesStatusSchema,#we import our marshmallow models
)
blueprint = Blueprint('kitchen', __name__, description='Kitchen Api')

schedules = [{
    'id': str(uuid.uuid4()),
    'scheduled': datetime.now(),
    'status': 'pending',
    'order': [
        {
            'product': 'capuccino',
            'quantity': 1,
            'size': 'big'
        }
    ]

}]


@blueprint.route('/kitchen/schedules')
class KitchenSchedules(MethodView):
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def get(self):
        return {
            'schedules': schedules
        }
    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=201, schema=GetScheduledOrdersSchema)
    def post(self, payload):
        return schedules[0]

@blueprint.route('/kitchen/schedules/<schedule_id>')
class KitchenSchedules(MethodView):
    @blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
    def get(self, schedule_id):
        return schedules[0]

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
    def put(self, payload, schedule_id):
        return schedules[0]
    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        return '', 204
@blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
@blueprint.route(
    '/kitchen/schedules/<schedule_id>/cancel', methods=['POST']

)
def cancel_schedule(schedule_id):
    return schedules[0], 200
@blueprint.response(status_code=200, schema=SchedulesStatusSchema)
@blueprint.route('/kitchen/schedules/<schedule_id>/status', methods=['GET'])
def get_schedule_status(schedule_id):
    return schedules[0], 200

