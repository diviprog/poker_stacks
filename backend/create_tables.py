# create_tables.py
import sys
import os

# ✅ Ensure `backend/` is in the Python module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database import Base, engine  # Use absolute imports
from backend.models import GameDB, PlayerDB  # Use absolute imports
def init_db():
    """Initialize the database by creating all tables"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
        # You can add any initial data here if needed
        
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")

if __name__ == "__main__":
    print("Starting database initialization...")
    init_db()

# Optional: Add a function to reset the database (helpful during development)
def reset_db():
    """Drop all tables and recreate them"""
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("Existing tables dropped.")
        
        # Recreate all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables recreated successfully!")
        
    except Exception as e:
        print(f"Error resetting database: {str(e)}")

# If you want to include a reset option when running the script
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print("Resetting database...")
        reset_db()
    else:
        print("Starting database initialization...")
        init_db()