from typing import Dict, Any

from twilio.rest import Client

from ..core.config import settings


class WhatsAppService:
    def __init__(self):
        self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        self.whatsapp_number = settings.twilio_whatsapp_number
    
    def send_message(self, to_phone: str, message: str) -> Dict[str, Any]:
        """Send a WhatsApp message"""
        try:
            message = self.client.messages.create(
                body=message,
                from_=f'whatsapp:{self.whatsapp_number}',
                to=f'whatsapp:{to_phone}'
            )
            return {"success": True, "message_sid": message.sid}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_menu_message(self, to_phone: str, menu_items: list) -> Dict[str, Any]:
        """Send formatted menu message"""
        message = f"🍽️ *{settings.restaurant_name} Menu* 🍽️\n\n"
        
        categories = {}
        for item in menu_items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        
        for category, items in categories.items():
            message += f"*{category.upper()}*\n"
            for item in items:
                message += f"• {item.name} - ₹{item.price:.2f}\n"
                if item.description:
                    message += f"  {item.description}\n"
                message += f"  ⏱️ {item.preparation_time} mins\n\n"
        
        message += "\n📝 To order, reply with:\n"
        message += "ORDER <item_name> <quantity> <your_address>\n\n"
        message += "Example: ORDER Biryani 2 123 Main Street, City"
        
        return self.send_message(to_phone, message)
    
    def send_order_confirmation(self, to_phone: str, order_data: dict) -> Dict[str, Any]:
        """Send order confirmation message"""
        message = "✅ *Order Confirmed!*\n\n"
        message += f"Order ID: #{order_data['id']}\n"
        message += f"Total: ₹{order_data['total_amount']:.2f}\n"
        message += f"Delivery Address: {order_data['delivery_address']}\n\n"
        
        message += "*Items:*\n"
        for item in order_data['items']:
            message += f"• {item['menu_item']['name']} x{item['quantity']}\n"
        
        message += "\n🚚 Estimated delivery: 30-45 minutes\n"
        message += f"📞 Contact: {settings.twilio_whatsapp_number}"
        
        return self.send_message(to_phone, message)

whatsapp_service = WhatsAppService()