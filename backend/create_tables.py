# create_tables.py
from database import Base, engine
from models import GameDB, PlayerDB  # Import your models

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