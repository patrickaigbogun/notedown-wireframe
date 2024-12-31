from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from pathlib import Path

# Get the correct path to .env file
env_path = Path(__file__).parent.parent / '.env'

# Load the environment variables from the .env file
load_dotenv(env_path)

# Set default database URL if not found in environment
DEFAULT_DB_URL = "postgresql://avnadmin:AVNS_u5si5zKjSYxhU2v1FuG@pg-26eae491-osasinnook-8e1a.k.aivencloud.com:17581/defaultdb?sslmode=require"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# Replace postgres:// with postgresql://
DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# Connect to the PostgreSQL database using SQLAlchemy
engine = create_engine(DATABASE_URL)
print("Database URL loaded successfully!")
