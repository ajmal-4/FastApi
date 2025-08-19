from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....api.deps import get_database
from ....crud.crud_menu import menu_item, category
from ....schemas.menu import MenuItem, MenuItemCreate, MenuItemUpdate, Category, CategoryCreate, CategoryUpdate

router = APIRouter()

@router.get("/", response_model=List[MenuItem])
def get_menu(db: Session = Depends(get_database())):
    """Get all available menu items"""
    return menu_item.get_available_items(db)

@router.get("/category/{category}", response_model=List[MenuItem])
def get_menu_by_category(category_id: str, db: Session = Depends(get_database())):
    """Get menu items by category"""
    return menu_item.get_by_category(db, category_id=category_id)

@router.post("/", response_model=MenuItem)
def create_menu_item(item: MenuItemCreate, db: Session = Depends(get_database())):
    """Create a new menu item"""
    return menu_item.create(db, obj_in=item)

@router.put("/{item_id}", response_model=MenuItem)
def update_menu_item(item_id: int, item: MenuItemUpdate, db: Session = Depends(get_database())):
    """Update an existing menu item"""

    # Get the existing DB object
    db_item = menu_item.get(db, id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Update the item
    updated_item = menu_item.update(db, db_obj=db_item, obj_in=item)
    return updated_item

@router.delete("/{item_id}", response_model=MenuItem)
def delete_menu_item(item_id: int, db: Session = Depends(get_database())):
    """Soft delete a menu item (mark as unavailable)"""
    # Get the existing DB object
    db_item = menu_item.get(db, id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    updated_item = menu_item.update(db, db_obj=db_item, obj_in={"is_available": False})
    return updated_item

# Categories
# ----------------

@router.get("/category", response_model=List[Category])
def get_all_categories(db: Session = Depends(get_database())):
    """List all the categories"""
    return category.get_multi(db)

# Add a new category
@router.post("/category", response_model=Category)
def create_category(item: CategoryCreate, db: Session = Depends(get_database())):
    """Create a new category"""
    return category.create(db, obj_in=item)

@router.put("/category/{category_id}", response_model=Category)
def update_category(category_id: int, item: CategoryUpdate, db: Session = Depends(get_database())):
    """Update an existing category"""

    # Get the existing DB object
    db_item = category.get(db, id=category_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Update the item
    updated_item = category.update(db, db_obj=db_item, obj_in=item)
    return updated_item