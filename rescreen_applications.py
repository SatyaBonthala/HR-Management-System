"""
Re-screen all applications stuck in SCREENING status
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database import SessionLocal
from models import JobApplication, Candidate, JobPosition
from agents import recruitment_agent
from datetime import datetime

def rescreen_all():
    db = SessionLocal()
    try:
        # Get all applications in SCREENING status
        applications = db.query(JobApplication).filter(
            JobApplication.status == "SCREENING"
        ).all()
        
        print(f"Found {len(applications)} applications to re-screen\n")
        
        for app in applications:
            try:
                print(f"Processing application {app.id}...")
                
                # Get candidate and position
                candidate = db.query(Candidate).filter(Candidate.id == app.candidate_id).first()
                position = db.query(JobPosition).filter(JobPosition.id == app.position_id).first()
                
                if not candidate or not position:
                    print(f"  ❌ Candidate or position not found")
                    continue
                
                print(f"  Candidate: {candidate.name}")
                print(f"  Position: {position.title}")
                
                # Run AI screening
                result = recruitment_agent.screen_candidate(
                    resume_text=candidate.resume_text or "No resume provided",
                    job_description=position.description,
                    required_skills=position.required_skills,
                    experience_required=position.experience_required
                )
                
                # Update application with screening results
                app.screening_notes = result.get("screening_notes", "")
                app.strengths = result.get("strengths", [])
                app.concerns = result.get("concerns", [])
                app.recommendation = result.get("recommendation", "unknown")
                
                # Update status based on recommendation
                recommendation = result.get("recommendation", "").lower()
                if recommendation == "recommend":
                    app.status = "INTERVIEW"
                elif recommendation == "maybe" or recommendation == "review":
                    app.status = "INTERVIEW"
                else:
                    app.status = "REJECTED"
                    
                app.updated_at = datetime.utcnow()
                
                # Update candidate profile
                candidate.ai_summary = result.get("ai_summary", "")
                candidate.match_score = result.get("match_score", 0)
                candidate.skills = result.get("skills", [])
                candidate.experience_years = result.get("experience_years", 0)
                
                db.commit()
                
                print(f"  ✅ Screening completed! Match score: {result.get('match_score')}, Recommendation: {result.get('recommendation')}")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                db.rollback()
                continue
        
        print(f"\n✅ Re-screening completed for all applications!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    rescreen_all()
