"""
Test AI screening manually
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from database import SessionLocal
from models import JobApplication, Candidate, JobPosition
from agents import recruitment_agent

def test_screening():
    db = SessionLocal()
    try:
        # Get first application
        app = db.query(JobApplication).first()
        if not app:
            print("No applications found")
            return
        
        print(f"Testing screening for application {app.id}")
        
        # Get candidate and position
        candidate = db.query(Candidate).filter(Candidate.id == app.candidate_id).first()
        position = db.query(JobPosition).filter(JobPosition.id == app.position_id).first()
        
        if not candidate or not position:
            print("Candidate or position not found")
            return
        
        print(f"Candidate: {candidate.name}")
        print(f"Position: {position.title}")
        print(f"Resume text available: {bool(candidate.resume_text)}")
        print(f"Resume length: {len(candidate.resume_text) if candidate.resume_text else 0}")
        
        # Run screening
        print("\nRunning AI screening...")
        result = recruitment_agent.screen_candidate(
            resume_text=candidate.resume_text or "No resume provided",
            job_description=position.description,
            required_skills=position.required_skills,
            experience_required=position.experience_required
        )
        
        print("\n✅ Screening completed!")
        print(f"Result keys: {result.keys()}")
        print(f"Match score: {result.get('match_score')}")
        print(f"Summary: {result.get('ai_summary', 'N/A')[:100]}")
        print(f"Strengths: {len(result.get('strengths', []))} items")
        print(f"Concerns: {len(result.get('concerns', []))} items")
        print(f"Recommendation: {result.get('recommendation')}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_screening()
