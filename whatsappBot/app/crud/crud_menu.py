from typing import List
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.menu import MenuItem, Category
from ..schemas.menu import MenuItemCreate, MenuItemUpdate, CategoryCreate, CategoryUpdate

class CRUDMenuItem(CRUDBase[MenuItem, MenuItemCreate, MenuItemUpdate]):
    def get_by_category(self, db: Session, *, category_id: int) -> List[MenuItem]:
        """ Get menu by category """
        return db.query(MenuItem).filter(
            MenuItem.category_id == category_id,
            MenuItem.is_available
        ).all()
    
    def get_available_items(self, db: Session) -> List[MenuItem]:
        """ get all the available items """
        return db.query(MenuItem).filter(MenuItem.is_available).all()

menu_item = CRUDMenuItem(MenuItem)

class CRUDCategories(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass

category = CRUDCategories(Category)