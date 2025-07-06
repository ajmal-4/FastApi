import re
from sqlalchemy.orm import Session

from ..crud.crud_menu import menu_item
from ..crud.crud_order import order
from ..schemas.order import OrderCreate, OrderItemCreate
from .whatsapp_service import whatsapp_service

class OrderService:
    def parse_order_message(self, message: str) -> dict:
        """Parse order message from WhatsApp"""
        # Expected format: ORDER <item_name> <quantity> <address>
        pattern = r'ORDER\s+(.+?)\s+(\d+)\s+(.+)'
        match = re.match(pattern, message, re.IGNORECASE)
        
        if not match:
            return {"success": False, "error": "Invalid order format"}
        
        item_name = match.group(1).strip()
        quantity = int(match.group(2))
        address = match.group(3).strip()
        
        return {
            "success": True,
            "item_name": item_name,
            "quantity": quantity,
            "address": address
        }
    
    def process_order(self, db: Session, phone: str, message: str, customer_name: str = None) -> dict:
        """Process incoming order"""
        parsed = self.parse_order_message(message)
        
        if not parsed["success"]:
            return parsed
        
        # Find menu item
        menu_items = menu_item.get_available_items(db)
        found_item = None
        
        for item in menu_items:
            if parsed["item_name"].lower() in item.name.lower():
                found_item = item
                break
        
        if not found_item:
            return {"success": False, "error": "Item not found in menu"}
        
        # Create order
        order_data = OrderCreate(
            customer_phone=phone,
            customer_name=customer_name,
            delivery_address=parsed["address"],
            items=[
                OrderItemCreate(
                    menu_item_id=found_item.id,
                    quantity=parsed["quantity"]
                )
            ]
        )
        
        try:
            new_order = order.create_with_items(db, obj_in=order_data)
            
            # Send confirmation
            order_dict = {
                "id": new_order.id,
                "total_amount": new_order.total_amount,
                "delivery_address": new_order.delivery_address,
                "items": [
                    {
                        "menu_item": {"name": found_item.name},
                        "quantity": parsed["quantity"]
                    }
                ]
            }
            
            whatsapp_service.send_order_confirmation(phone, order_dict)
            
            return {"success": True, "order_id": new_order.id}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

order_service = OrderService()