from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....api.deps import get_database
from ....crud.crud_order import order
from ....schemas.order import Order, OrderCreate

router = APIRouter()

@router.get("/", response_model=List[Order])
def get_orders(db: Session = Depends(get_database())):
    """Get all orders"""
    return order.get_multi(db)

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_database())):
    """Get specific order"""
    db_order = order.get(db, id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/", response_model=Order)
def create_order(order_data: OrderCreate, db: Session = Depends(get_database())):
    """Create a new order"""
    return order.create_with_items(db, obj_in=order_data)