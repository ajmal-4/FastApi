from pathlib import Path
from pydantic_settings import BaseSettings

# Get the absolute path to the current file
current_file = Path(__file__).resolve()

# Move up three levels to reach project root
project_dir = current_file.parents[2]

# Construct .env path
env_path = project_dir / ".env"
# Sqlite path
db_path = project_dir / "restaurant.db"

class Settings(BaseSettings):
    # Database
    database_url: str = ""
    
    # WhatsApp API
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_number: str = ""
    
    # Restaurant settings
    restaurant_name: str = "Delicious Bites"
    delivery_radius_km: float = 10.0
    
    class Config:
        env_file = env_path
        case_sensitive = False
        extra = "allow"

settings = Settings()