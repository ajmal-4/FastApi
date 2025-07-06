from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_phone = Column(String(20), nullable=False)
    customer_name = Column(String(100))
    delivery_address = Column(Text, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, preparing, delivered, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    delivery_time = Column(DateTime)
    
    # Relationship with order items
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    special_instructions = Column(Text)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")