#!/usr/bin/env python3
"""
Test script to manually verify database table creation.
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("Testing database table creation...")
    
    # Import models to register them with SQLAlchemy
    from app.models import user
    from app.database import create_tables, engine
    
    print(f"Database URL: {engine.url}")
    print("Creating tables...")
    create_tables()
    
    # Check if table exists
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Existing tables: {tables}")
    
    if 'users' in tables:
        print("✅ Users table created successfully!")
        # Test basic User creation
        from app.database import get_db
        from app.models.user import User
        
        db = next(get_db())
        test_user = User(
            email="test@example.com",
            name="Test User",
            password_hash="dummy_hash"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ Created test user with ID: {test_user.id}")
        
        # Clean up
        db.delete(test_user)
        db.commit()
        db.close()
    else:
        print("❌ Users table was not created!")
