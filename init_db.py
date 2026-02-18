"""
Database initialization script
Run this to create all tables
"""
from database import Base, engine
from models import Candidate, JobPosition, JobApplication, Employee, OnboardingProcess

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")
    print("\nTables created:")
    print("  - candidates")
    print("  - job_positions")
    print("  - job_applications")
    print("  - employees")
    print("  - onboarding_processes")
    print("\nYou can now run the application with: python main.py")

if __name__ == "__main__":
    init_db()
