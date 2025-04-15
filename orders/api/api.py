from datetime import datetime
from http import HTTPStatus
from uuid import UUID
import time
import uuid
from fastapi import HTTPException
from fastapi import APIRouter  # Use APIRouter instead of FastAPI
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema,
)

# Create an APIRouter instance
api = APIRouter()

# Sample Order Dictionary

ORDERS = []

@app.get('/orders', response_model=GetOrdersSchema)
def get_orders():
    return ORDERS  # Return a dictionary with a list of orders

@app.post('/orders',
           status_code=status.HTTP_201_CREATED,
           response_model=GetOrderSchema)
def create_order(order_details: CreateOrderSchema):
    # You can modify this to add the created order to a database
    # Return the same order for now
    order = order_details.dict()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.now()
    order['status'] = 'created'
    ORDERS.append(order)
    return order

@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            return order
        raise HTTPException(
            status_code=404, detail=f'Order with ID{order_id} not found'
        )
    # Return the order based on its ID (can be dynamic)

@app.put('/orders/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order
        raise HTTPException(
            status_code=404, detail=f'Order with ID{order_id} not found'
        )
    # You can modify the order here (update) and return the updated order
   
@app.delete(
        '/orders/{order_id}',
          status_code=status.HTTP_204_NO_CONTENT,
          response_class=Response,
          )
def delete_order(order_id: UUID):
    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            return Response(status_code=HTTPStatus.NO_CONTENT.value)
        raise HTTPException(
            status_code=404, detail=f'Order with ID {order_id} not found'

        )
    # Logic to delete the order
    return Response(status_code=HTTPStatus.NO_CONTENT.value)

@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )
    return order  # Logic for payment (you can extend it as needed)

@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order
        raise HTTPException(
            status_code=404, detail=f'Order with ID {order_id} not found'
        )
     # Logic to cancel the order (you can extend it as needed)
