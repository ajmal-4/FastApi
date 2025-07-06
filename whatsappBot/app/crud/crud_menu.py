from typing import List
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.menu import MenuItem
from ..schemas.menu import MenuItemCreate, MenuItemUpdate

class CRUDMenuItem(CRUDBase[MenuItem, MenuItemCreate, MenuItemUpdate]):
    def get_by_category(self, db: Session, *, category: str) -> List[MenuItem]:
        return db.query(MenuItem).filter(
            MenuItem.category == category,
            MenuItem.is_available == True
        ).all()
    
    def get_available_items(self, db: Session) -> List[MenuItem]:
        return db.query(MenuItem).filter(MenuItem.is_available == True).all()

menu_item = CRUDMenuItem(MenuItem)