from sqlalchemy.orm import Session
from ..core.database import SessionLocal, engine, Base
from ..models.menu import MenuItem, Category

def seed_categories(db: Session):
    category_names = ["Pizza", "Burger", "Beverage"]
    categories = []
    for name in category_names:
        existing = db.query(Category).filter_by(name=name).first()
        if not existing:
            category = Category(name=name)
            db.add(category)
            db.flush()  # get ID without committing
            categories.append(category)
        else:
            categories.append(existing)
    db.commit()
    return {cat.name: cat.id for cat in categories}  # return mapping name -> id


def seed_menu_items(db: Session):
    category_map = seed_categories(db)

    items = [
        {
            "name": "Margherita Pizza",
            "description": "Classic delight with 100% real mozzarella cheese",
            "price": 249.0,
            "category_id": category_map["Pizza"],
            "image_url": "https://example.com/margherita.jpg",
            "is_available": True,
            "preparation_time": 15
        },
        {
            "name": "Veggie Burger",
            "description": "Loaded with fresh veggies and signature sauce",
            "price": 149.0,
            "category_id": category_map["Burger"],
            "image_url": "https://example.com/veggieburger.jpg",
            "is_available": True,
            "preparation_time": 10
        },
        {
            "name": "Cold Coffee",
            "description": "Chilled coffee with whipped cream topping",
            "price": 99.0,
            "category_id": category_map["Beverage"],
            "image_url": "https://example.com/coldcoffee.jpg",
            "is_available": True,
            "preparation_time": 5
        }
    ]

    for item in items:
        existing_item = db.query(MenuItem).filter_by(name=item["name"]).first()
        if not existing_item:
            db_item = MenuItem(**item)
            db.add(db_item)
    db.commit()

def seed():
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_menu_items(db)
        print("✅ Database seeding completed of categories and menu items.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
