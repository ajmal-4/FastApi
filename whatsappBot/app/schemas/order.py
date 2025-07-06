from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .menu import MenuItem

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int
    special_instructions: Optional[str] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    quantity: Optional[int] = None
    special_instructions: Optional[str] = None

class OrderItem(OrderItemBase):
    id: int
    price: float
    menu_item: MenuItem

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_phone: str
    customer_name: Optional[str] = None
    delivery_address: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    customer_phone: Optional[str] = None
    customer_name: Optional[str] = None
    delivery_address: Optional[str] = None
    items: Optional[List[OrderItemUpdate]] = None
    status: Optional[str] = None
    delivery_time: Optional[datetime] = None

class Order(OrderBase):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    delivery_time: Optional[datetime] = None
    items: List[OrderItem] = []

    class Config:
        from_attributes = True
