from typing import List
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.order import Order, OrderItem
from ..schemas.order import OrderCreate, OrderUpdate
from ..models.menu import MenuItem

class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def create_with_items(self, db: Session, *, obj_in: OrderCreate) -> Order:
        # Create order
        order_data = obj_in.dict(exclude={'items'})
        db_order = Order(**order_data)
        db.add(db_order)
        db.flush()  # To get the order ID
        
        # Add order items and calculate total
        total_amount = 0
        for item_data in obj_in.items:
            # Get menu item price
            menu_item = db.query(MenuItem).filter(MenuItem.id == item_data.menu_item_id).first()
            if menu_item:
                item_price = menu_item.price * item_data.quantity
                total_amount += item_price
                
                db_order_item = OrderItem(
                    order_id=db_order.id,
                    menu_item_id=item_data.menu_item_id,
                    quantity=item_data.quantity,
                    price=item_price,
                    special_instructions=item_data.special_instructions
                )
                db.add(db_order_item)
        
        db_order.total_amount = total_amount
        db.commit()
        db.refresh(db_order)
        return db_order
    
    def get_by_phone(self, db: Session, *, phone: str) -> List[Order]:
        return db.query(Order).filter(Order.customer_phone == phone).all()

order = CRUDOrder(Order)