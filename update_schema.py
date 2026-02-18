"""
Update database schema to add salary_range column to job_positions table
"""
from database import engine
from sqlalchemy import text

def update_schema():
    """Add salary_range column if it doesn't exist"""
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='job_positions' AND column_name='salary_range'
        """))
        
        if result.fetchone() is None:
            # Add the column
            conn.execute(text("""
                ALTER TABLE job_positions 
                ADD COLUMN salary_range VARCHAR(100)
            """))
            conn.commit()
            print("✅ Added salary_range column to job_positions table")
        else:
            print("✅ salary_range column already exists")

if __name__ == "__main__":
    update_schema()
