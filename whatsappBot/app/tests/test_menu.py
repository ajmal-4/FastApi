import sqlite3
from pathlib import Path

current_file = Path(__file__).resolve()
project_dir = current_file.parents[2]
db_path = project_dir / "restaurant.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

res = cursor.execute("SELECT * FROM menu_items;")
results = res.fetchall()

for result in results:
    print(f"\n {result}")