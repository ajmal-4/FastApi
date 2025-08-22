from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from ....api.deps import get_database 
from ....crud.crud_menu import menu_item
from ....core.config import settings
from ....services.whatsapp_service import whatsapp_service
from ....services.order_service import order_service

router = APIRouter()

VERIFY_TOKEN = "sample_token"  # you decide this string

@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    Meta will send a GET request with hub.mode, hub.challenge, and hub.verify_token
    """
    params = request.query_params
    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == VERIFY_TOKEN
    ):
        return int(params.get("hub.challenge"))
    return {"error": "Invalid verification token"}

@router.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_database)):
    """Handle incoming WhatsApp messages"""
    try:
        form_data = await request.form()
        
        # Extract message data
        from_number = form_data.get("from", "").replace("whatsapp:", "")
        message_body = form_data.get("body", "").strip()
        profile_name = form_data.get("profile_name", "")
        
        if not from_number or not message_body:
            raise HTTPException(status_code=400, detail="Invalid message data")
        
        # Handle different message types
        if message_body.upper() == "MENU":
            # Send menu
            menu_items = menu_item.get_available_items(db)
            whatsapp_service.send_menu_message(from_number, menu_items)
            
        elif message_body.upper().startswith("ORDER"):
            # Process order
            result = order_service.process_order(db, from_number, message_body, profile_name)
            
            if not result["success"]:
                error_msg = f"❌ Order failed: {result['error']}\n\n"
                error_msg += "Please use format: ORDER <item_name> <quantity> <address>\n"
                error_msg += "Type MENU to see available items."
                whatsapp_service.send_message(from_number, error_msg)
        
        else:
            # Welcome message
            welcome_msg = f"👋 Welcome to {settings.restaurant_name}!\n\n"
            welcome_msg += "🍽️ Type MENU to see our delicious items\n"
            welcome_msg += "📝 Type ORDER <item_name> <quantity> <address> to place an order\n\n"
            welcome_msg += "Example: ORDER Biryani 2 123 Main Street, City"
            whatsapp_service.send_message(from_number, welcome_msg)
        
        return {"status": "success"}
    
    except HTTPException:
        raise
        
    except Exception as e:
        return {"status": "error", "message": str(e)}