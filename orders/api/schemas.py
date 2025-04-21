from enum import Enum
from typing import Annotated, List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

# Define the possible sizes
class Size(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"

# Define possible order statuses
class Status(str, Enum):
    created = 'created'
    progress = 'progress'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'

# Order item schema
class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Annotated[int, Field(ge=1, strict=True)] = 1

    class Config:
        extra = 'forbid' #

    @field_validator('quantity', mode='before')
    @classmethod
    def quantity_non_nullable(cls, value):
        if value is None or value < 1:
            raise ValueError('Quantity must be a positive number and may not be None')
        return value

# Schema to create orders, which expects a list of items
class CreateOrderSchema(BaseModel):
    order: List[OrderItemSchema] = Field(..., min_items=1)
    class Config:
        extra = 'forbid'

# Schema for retrieving a single order with an ID, creation date, and status
class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: Status

# Schema for returning a list of orders
class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema] = []
