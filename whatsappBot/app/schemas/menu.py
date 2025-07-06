from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    image_url: Optional[str] = None
    is_available: bool = True
    preparation_time: int = 15

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = None

class MenuItem(MenuItemBase):
    id: int

    class Config:
        from_attributes = True
