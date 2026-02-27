"""
Migration script to add is_active field to employees table
Run this script once to update existing database
"""
from database import SessionLocal, engine
from sqlalchemy import text

def add_is_active_column():
    """Add is_active column to employees table"""
    db = SessionLocal()
    try:
        # Check if column exists
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='employees' AND column_name='is_active'
        """))
        
        if result.fetchone() is None:
            # Add column if it doesn't exist
            print("Adding is_active column to employees table...")
            db.execute(text("""
                ALTER TABLE employees 
                ADD COLUMN is_active BOOLEAN DEFAULT TRUE
            """))
            db.commit()
            print("✓ Successfully added is_active column")
            
            # Update existing employees to be active
            print("Setting all existing employees to active...")
            db.execute(text("UPDATE employees SET is_active = TRUE WHERE is_active IS NULL"))
            db.commit()
            print("✓ Successfully updated existing employees")
        else:
            print("is_active column already exists. No migration needed.")
            
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database migration...")
    add_is_active_column()
    print("Migration complete!")
