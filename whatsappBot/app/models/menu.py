from sqlalchemy import Column, Integer, String, Float, Boolean, Text

from ..core.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    image_url = Column(String(200))
    is_available = Column(Boolean, default=True)
    preparation_time = Column(Integer, default=15)  # minutes