from datetime import datetime
from http import HTTPStatus
from uuid import UUID
from typing import Optional
import uuid
from fastapi import HTTPException, APIRouter
from starlette.responses import Response
from starlette import status

from orders.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema,
)

# Create an APIRouter instance
api = APIRouter()

# Sample Order Dictionary
orders = []

@api.get('/orders', response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int]= None):
    if cancelled is None and limit is None:# if the parameters  havent been set , we return immediately
        return {'orders': orders}  # Return a dictionary with a list of orders
    
    query_set =[order for order in orders] # if any of the parameters has been set we filterr list into a query_set

    if cancelled is not None:
        if cancelled:
            query_set =[
                order
                for order in query_set
                if order['status'] == 'cancelled'
            ]
        else:
            query_set = [
                order
                for order in query_set
                if order['status'] != 'cancelled'
            ]
    if limit is not None and len(query_set) > limit: #if limit is set and its value is lower that the length of query_set, we return a subset of query_set.
        return{'orders': query_set[:limit]}
    return {'orders': query_set}

@api.post('/orders',
          status_code=status.HTTP_201_CREATED,
          response_model=GetOrderSchema)
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.now()
    order['status'] = 'created'
    orders.append(order)
    return order

@api.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in orders:
        if order['id'] == order_id:
            return order
    # Raise the exception after checking all orders
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@api.put('/orders/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in orders:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order
