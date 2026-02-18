"""
Main FastAPI application for Agentic HR Management System
"""
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime

from config import settings
from database import get_db, engine, Base
from models import (
    Candidate, JobPosition, JobApplication, Employee, 
    OnboardingProcess, ApplicationStatus, OnboardingStatus
)
from schemas import (
    CandidateCreate, CandidateResponse,
    JobPositionCreate, JobPositionResponse,
    JobApplicationCreate, JobApplicationResponse,
    EmployeeCreate, EmployeeResponse,
    OnboardingMessage, OnboardingResponse, OnboardingChatResponse
)
from agents import recruitment_agent, onboarding_agent

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered HR Management System with intelligent agents for recruitment and onboarding",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/")
def root():
    """Root endpoint - health check"""
    return {
        "message": "Agentic HR Management System API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


# ============================================================================
# JOB POSITIONS
# ============================================================================

@app.post("/positions/", response_model=JobPositionResponse, status_code=201)
def create_job_position(position: JobPositionCreate, db: Session = Depends(get_db)):
    """Create a new job position"""
    db_position = JobPosition(**position.model_dump())
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position


@app.get("/positions/", response_model=List[JobPositionResponse])
def list_job_positions(skip: int = 0, limit: int = 100, 
                       active_only: bool = True, db: Session = Depends(get_db)):
    """List all job positions"""
    query = db.query(JobPosition)
    if active_only:
        query = query.filter(JobPosition.is_active == True)
    positions = query.offset(skip).limit(limit).all()
    return positions


@app.get("/positions/{position_id}", response_model=JobPositionResponse)
def get_job_position(position_id: int, db: Session = Depends(get_db)):
    """Get a specific job position"""
    position = db.query(JobPosition).filter(JobPosition.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


# ============================================================================
# CANDIDATES
# ============================================================================

@app.post("/candidates/", response_model=CandidateResponse, status_code=201)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    """Create a new candidate"""
    # Check if candidate already exists
    existing = db.query(Candidate).filter(Candidate.email == candidate.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Candidate with this email already exists")
    
    db_candidate = Candidate(**candidate.model_dump())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@app.get("/candidates/", response_model=List[CandidateResponse])
def list_candidates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all candidates"""
    candidates = db.query(Candidate).offset(skip).limit(limit).all()
    return candidates


@app.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Get a specific candidate"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


# ============================================================================
# JOB APPLICATIONS & AI SCREENING
# ============================================================================

@app.post("/applications/", response_model=JobApplicationResponse, status_code=201)
def create_application(
    application: JobApplicationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submit a job application and trigger AI screening
    """
    # Verify candidate and position exist
    candidate = db.query(Candidate).filter(Candidate.id == application.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    position = db.query(JobPosition).filter(JobPosition.id == application.position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    # Check for duplicate application
    existing = db.query(JobApplication).filter(
        JobApplication.candidate_id == application.candidate_id,
        JobApplication.position_id == application.position_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Application already exists")
    
    # Create application
    db_application = JobApplication(**application.model_dump())
    db_application.status = ApplicationStatus.SUBMITTED
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    # Schedule AI screening in background
    background_tasks.add_task(
        screen_application_with_ai,
        db_application.id,
        candidate.resume_text,
        position.description,
        position.required_skills,
        position.experience_required
    )
    
    return db_application


def screen_application_with_ai(
    application_id: int,
    resume_text: str,
    job_description: str,
    required_skills: List[str],
    experience_required: int
):
    """
    Background task to screen application with AI agent
    """
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        # Get application
        application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
        if not application:
            return
        
        # Update status
        application.status = ApplicationStatus.SCREENING
        db.commit()
        
        # Run AI screening
        if not resume_text:
            resume_text = "No resume text provided"
        
        screening_result = recruitment_agent.screen_candidate(
            resume_text=resume_text,
            job_description=job_description,
            required_skills=required_skills,
            experience_required=experience_required
        )
        
        # Update application with results
        application.screening_notes = screening_result.get("screening_notes", "")
        application.strengths = screening_result.get("strengths", [])
        application.concerns = screening_result.get("concerns", [])
        application.recommendation = screening_result.get("recommendation", "review")
        
        # Update candidate with extracted info
        candidate = application.candidate
        candidate.skills = screening_result.get("skills", [])
        candidate.experience_years = screening_result.get("experience_years", 0)
        candidate.ai_summary = screening_result.get("ai_summary", "")
        candidate.match_score = screening_result.get("match_score", 50)
        
        db.commit()
        
    except Exception as e:
        print(f"Error in AI screening: {str(e)}")
        db.rollback()
    finally:
        db.close()


@app.get("/applications/", response_model=List[JobApplicationResponse])
def list_applications(
    position_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List job applications with optional filters"""
    query = db.query(JobApplication)
    
    if position_id:
        query = query.filter(JobApplication.position_id == position_id)
    if status:
        query = query.filter(JobApplication.status == status)
    
    applications = query.offset(skip).limit(limit).all()
    return applications


@app.get("/applications/{application_id}", response_model=JobApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get a specific application"""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


# ============================================================================
# EMPLOYEES
# ============================================================================

@app.post("/employees/", response_model=EmployeeResponse, status_code=201)
def create_employee(
    employee: EmployeeCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new employee and initialize onboarding
    """
    # Check if employee already exists
    existing = db.query(Employee).filter(Employee.email == employee.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee with this email already exists")
    
    # Generate employee ID
    employee_count = db.query(Employee).count()
    employee_id = f"EMP{employee_count + 1:05d}"
    
    db_employee = Employee(
        **employee.model_dump(),
        employee_id=employee_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    # Schedule onboarding initialization in background
    background_tasks.add_task(
        initialize_onboarding,
        db_employee.id,
        {
            "name": db_employee.name,
            "position": db_employee.position,
            "department": db_employee.department,
            "hire_date": db_employee.hire_date.isoformat()
        }
    )
    
    return db_employee


def initialize_onboarding(employee_id: int, employee_data: dict):
    """
    Background task to initialize onboarding with AI agent
    """
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        # Create onboarding checklist with AI
        checklist_result = onboarding_agent.create_onboarding_checklist(employee_data)
        
        # Create onboarding record
        onboarding = OnboardingProcess(
            employee_id=employee_id,
            status=OnboardingStatus.PENDING,
            checklist=checklist_result.get("checklist", []),
            completed_tasks=[],
            next_steps=checklist_result.get("next_steps", ""),
            start_date=datetime.utcnow()
        )
        
        db.add(onboarding)
        db.commit()
        
    except Exception as e:
        print(f"Error initializing onboarding: {str(e)}")
        db.rollback()
    finally:
        db.close()


@app.get("/employees/", response_model=List[EmployeeResponse])
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all employees"""
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get a specific employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


# ============================================================================
# ONBOARDING
# ============================================================================

@app.get("/employees/{employee_id}/onboarding", response_model=OnboardingResponse)
def get_onboarding(employee_id: int, db: Session = Depends(get_db)):
    """Get onboarding information for an employee"""
    onboarding = db.query(OnboardingProcess).filter(
        OnboardingProcess.employee_id == employee_id
    ).first()
    
    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding process not found")
    
    return onboarding


@app.post("/employees/{employee_id}/onboarding/query", response_model=OnboardingChatResponse)
def onboarding_chat(
    employee_id: int,
    message_data: OnboardingMessage,
    db: Session = Depends(get_db)
):
    """
    Chat with the onboarding AI agent
    """
    # Get employee and onboarding
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    onboarding = db.query(OnboardingProcess).filter(
        OnboardingProcess.employee_id == employee_id
    ).first()
    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")
    
    # Get conversation history
    conversation_history = onboarding.interaction_history or []
    
    # Get AI response
    employee_data = {
        "name": employee.name,
        "position": employee.position,
        "department": employee.department,
        "hire_date": employee.hire_date.isoformat()
    }
    
    response = onboarding_agent.handle_onboarding_query(
        employee_data=employee_data,
        message=message_data.message,
        conversation_history=conversation_history
    )
    
    # Update conversation history
    conversation_history.append({
        "role": "employee",
        "content": message_data.message,
        "timestamp": response["timestamp"]
    })
    conversation_history.append({
        "role": "agent",
        "content": response["response"],
        "timestamp": response["timestamp"]
    })
    
    onboarding.interaction_history = conversation_history
    onboarding.status = OnboardingStatus.IN_PROGRESS
    db.commit()
    
    return OnboardingChatResponse(
        response=response["response"],
        updated_status=onboarding.status.value,
        next_steps=onboarding.next_steps
    )


@app.post("/employees/{employee_id}/onboarding/checklist")
def create_onboarding_checklist(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Generate AI onboarding checklist for employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee_data = {
        "name": employee.name,
        "position": employee.position,
        "department": employee.department,
        "hire_date": employee.hire_date.isoformat()
    }
    
    result = onboarding_agent.create_onboarding_checklist(employee_data)
    
    # Update onboarding process
    onboarding = db.query(OnboardingProcess).filter(
        OnboardingProcess.employee_id == employee_id
    ).first()
    
    if onboarding:
        onboarding.checklist = result.get("checklist", [])
        onboarding.next_steps = result.get("next_steps", "")
        db.commit()
    
    return result


@app.post("/employees/{employee_id}/onboarding/progress")
def update_onboarding_progress(
    employee_id: int,
    completed_tasks: List[str],
    db: Session = Depends(get_db)
):
    """Update onboarding progress"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    onboarding = db.query(OnboardingProcess).filter(
        OnboardingProcess.employee_id == employee_id
    ).first()
    
    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")
    
    employee_data = {
        "name": employee.name,
        "position": employee.position,
        "hire_date": employee.hire_date.isoformat()
    }
    
    total_tasks = len(onboarding.checklist or [])
    result = onboarding_agent.update_onboarding_progress(
        employee_data,
        completed_tasks,
        total_tasks
    )
    
    return result


@app.post("/employees/{employee_id}/onboarding/complete-task")
def complete_onboarding_task(
    employee_id: int,
    task_id: str,
    db: Session = Depends(get_db)
):
    """Mark an onboarding task as completed"""
    onboarding = db.query(OnboardingProcess).filter(
        OnboardingProcess.employee_id == employee_id
    ).first()
    
    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")
    
    completed_tasks = onboarding.completed_tasks or []
    if task_id not in completed_tasks:
        completed_tasks.append(task_id)
        onboarding.completed_tasks = completed_tasks
        
        # Check if all tasks completed
        total_tasks = len(onboarding.checklist or [])
        if len(completed_tasks) >= total_tasks and total_tasks > 0:
            onboarding.status = OnboardingStatus.COMPLETED
            onboarding.completion_date = datetime.utcnow()
        else:
            onboarding.status = OnboardingStatus.IN_PROGRESS
        
        db.commit()
    
    return {
        "success": True,
        "completed_tasks": len(completed_tasks),
        "total_tasks": len(onboarding.checklist or []),
        "status": onboarding.status.value
    }


# ============================================================================
# ANALYTICS
# ============================================================================

@app.get("/analytics/recruitment")
def get_recruitment_analytics(db: Session = Depends(get_db)):
    """Get recruitment analytics"""
    total_positions = db.query(JobPosition).count()
    active_positions = db.query(JobPosition).filter(JobPosition.is_active == True).count()
    total_candidates = db.query(Candidate).count()
    total_applications = db.query(JobApplication).count()
    
    # Applications by status
    applications_by_status = {}
    for status in ApplicationStatus:
        count = db.query(JobApplication).filter(JobApplication.status == status).count()
        applications_by_status[status.value] = count
    
    return {
        "total_positions": total_positions,
        "active_positions": active_positions,
        "total_candidates": total_candidates,
        "total_applications": total_applications,
        "applications_by_status": applications_by_status
    }


@app.get("/analytics/onboarding")
def get_onboarding_analytics(db: Session = Depends(get_db)):
    """Get onboarding analytics"""
    total_employees = db.query(Employee).count()
    total_onboarding = db.query(OnboardingProcess).count()
    
    # Onboarding by status
    onboarding_by_status = {}
    for status in OnboardingStatus:
        count = db.query(OnboardingProcess).filter(OnboardingProcess.status == status).count()
        onboarding_by_status[status.value] = count
    
    return {
        "total_employees": total_employees,
        "total_onboarding": total_onboarding,
        "onboarding_by_status": onboarding_by_status
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
