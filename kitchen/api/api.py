import uuid
from datetime import datetime
from click import progressbar
from flask.views import MethodView
from flask_smorest import Blueprint

from api.schema import (
	GetScheduledOrderSchema,
	ScheduleOrderSchema,
	GetScheduledOrdersSchema,
	SchedulesStatusSchema,
	GetKitchenScheduleParameters,
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


@blueprint.route('/kitchen/schedules')  # we use the Blueprint instance to define our routes
class KitchenSchedules(MethodView):
	@blueprint.arguments(GetKitchenScheduleParameters, location='query')
	@blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
	def get(self, parameters):
		if not parameters:
			return {'schedules': schedules}

		query_set = [schedule for schedule in schedules]

		in_progress = parameters.get('progress')
		if in_progress is not None:
			if in_progress:
				# Example filter: only return schedules with status 'in_progress'
				query_set = [
                    schedule for schedule in schedules
                    if schedule['status'] == 'progress'
                ]
			else:
				# Example filter: only return schedules NOT in 'progress'
				query_set = [
					schedule for schedule in schedules
					if schedule['status'] != 'progress'
				]

		since = parameters.get('since') if parameters else None
		if since is not None:
			query_set = [
				schedule for schedule in schedules
				if schedule['scheduled'] >= since
			]

		limit = parameters.get('limit') if parameters else None
		if isinstance(limit, int) and limit >   limit:
			query_set = query_set[:limit]

		return {'schedules': query_set}

	@blueprint.arguments(ScheduleOrderSchema)
	@blueprint.response(status_code=201, schema=GetScheduledOrderSchema)
	def post(self, payload):
		return schedules[0]

@blueprint.route('/kitchen/schedules/<schedule_id>')
class KitchenScheduleById(MethodView):
	@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
	def get(self, schedule_id):
		return schedules[0]

	@blueprint.arguments(ScheduleOrderSchema)
	@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
	def put(self, payload, schedule_id):
		return schedules[0]

	@blueprint.response(status_code=204)
	def delete(self, schedule_id):
		return '' , 204

@blueprint.route('/kitchen/schedules/<schedule_id>/cancel', methods=['POST'])
@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
def cancel_schedule(schedule_id):
	return schedules[0]

@blueprint.route('/kitchen/schedules/<schedule_id>/status', methods=['GET'])
@blueprint.response(status_code=200, schema=SchedulesStatusSchema)
def get_schedule_status(schedule_id):
	return {'status': schedules[0]['status']}

