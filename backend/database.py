import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import re

load_dotenv()

# Search for the env file in parent directory if not found
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

DATABASE_URL = os.getenv("SUPABASE_URL")

# Quick fix for postgres:// vs postgresql+psycopg2:// and password with brackets 
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    # Quick fix for password wrapped in brackets like [@onion.harry.03@]
    import urllib.parse
    if "[@" in DATABASE_URL and "@]" in DATABASE_URL:
        # Extract the password and URL encode it
        start_idx = DATABASE_URL.find(":[") + 2
        end_idx = DATABASE_URL.find("@]") + 1
        password = DATABASE_URL[start_idx:end_idx]
        encoded_password = urllib.parse.quote_plus(password)
        DATABASE_URL = DATABASE_URL.replace(f"[{password}]", encoded_password)
        
if not DATABASE_URL:
    print("WARNING: SUPABASE_URL not found in .env")
    DATABASE_URL = "sqlite:///./backend/db.sqlite3"  # fallback for safety

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
