from flask.views import MethodView
from flask_smorest import Blueprint
import uuid
import copy

from datetime import datetime
from marshmallow import ValidationError # we import the vaalidationErro class from marshmallow
from flask import abort
from api.schemas import(
    GetScheduledOrderSchema,
    ScheduleStatusSchema,
    ScheduleOrderSchema,
    GetKitchenScheduleParameters
)# we import our marshmallow models
schedules =[]
def validate_schedule(schedule):
    schedule = copy.deepcopy(schedule)
    schedule['scheduled'] = schedule['scheduled'].isoformat()
    errors = GetScheduledOrderSchema().validate(schedule)
    if errors:
        raise ValidationError(errors)
blueprint = Blueprint('kitchen', __name__, description='Kitchen API')

schedules = [{
    'id': str(uuid.uuid4()),
    'scheduled': datetime.now(),
    'status': 'pending',
    'order': [
        {
        'product': 'capuccino',
        'quantity':  1,
        'size': 'big'
        }
    ]
}]

@blueprint.route('/kitchen/schedules')  # Corrected the route
class KitchenSchedules(MethodView):

    @blueprint.arguments(GetKitchenScheduleParameters, location='query')
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)# we use the blueprints response() decorator to register a marshmallow model for the response payload
    def get(self, parameters):
        for schedule in schedules:
            schedule = copy.deepcopy(schedule)
            schedule['scheduled'] = schedule['scheduled'].isoformat()
            errors = GetScheduledOrderSchema().validate(schedule)
            if errors:
                raise ValidationError(errors)
            if not parameters: #if no parameters is set  we return the full list of schedules
             return {'schedules': schedules}
        query_set =[schedule for schedule in schedules] #if the user set any url query parameters, we use them to filter the list of schedules

        in_progress = parameters.get(progress) #we check for the presence of each url query parameter by using the dictionary's get() method
        if in_progress is not None:
            if in_progress:
                query_set =[
                    schedule for schedule in schedules
                    if schedule['status'] == 'progress'

                ]
            else:
                query_set=[
                    schedule for schedule in schedules
                    if schedule['status'] != 'progress'


             ]
        since = parameters.get('since')
        if since  is not None:
            query_set =[
                schedule for schedule in schedules
                if schedule['scheduled'] >=since
        ]
        limit = parameters.get('limit')
        if limit is not None and len(query_set)>limit:
            query_set= query_set[:limit]

        return {'schedules': query_set}



        
    


    
    @blueprint.arguments(ScheduleOrderSchema)# we use the blueprints arguements() decorator to register a marshmallow model for the request payload
    @blueprint.response(status_code=201, schema=GetScheduledOrderSchema) # we set the status_code parameter to the desired status code
    def post(self, payload):
        payload['id'] = str(uuid.uuid4())
        payload['scheduled'] = datetime.now()
        payload['status'] = 'pending'
        schedules.append(payload)
        validate_schedule(payload)
        return payload
    

@blueprint.route('/kitchen/schedules/<schedule_id>')  # Corrected the route
class KitchenSchedule(MethodView):
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def get(self, schedule_id):
        for schedule in schedules:
            if schedule['id'] == schedule_id:
                validate_schedule(schedule)
                return schedule
        abort (404, description= f'Resources with Id {schedule_id} not found')
            
        return schedules[0]
    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def put(self, payload, schedule_id):
        for schedule in schedules:
            if schedule['id'] == schedule_id:
                schedule.update(payload)
                validate_schedule(schedule)
                return schedule
        abort(404, description= f'Resource with id{schedule_id} not found')



        
    
    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        for index, schedule in enumerate(schedules):
            if schedule['id'] == schedule_id:
                schedule.pop(index)
                return
        abort(404, description=f'Resource with ID{schedule_id} not found')
        
@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
@blueprint.route('/kitchen/schedule/<schedule_id>/cancel', methods=['POST'])
def cancel_schedule(schedule_id):
    for schedule in schedules:
        if schedule['id']== schedule_id:
            schedule['status'] = 'cancelled'
            validate_schedule(schedule)
            return schedule
    abort(404, description=f'Resource with ID {schedule_id} not found')

   
@blueprint.response(status_code=200, schema=ScheduleOrderSchema)
@blueprint.route('/kitchen/schedules/<schedule_id>/status', methods=['GET'])  # Corrected methods
def get_schedule_status(schedule_id):
     for schedule in schedules:
         validate_schedule(schedule)
         return{'status': schedule['status']}
     abort(404, description=f'Resource with ID {schedule_id} not found')
    
