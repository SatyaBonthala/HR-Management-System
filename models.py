"""
Database models for the HR Management System
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


class ApplicationStatus(str, enum.Enum):
    """Status of a job application"""
    SUBMITTED = "submitted"
    SCREENING = "screening"
    INTERVIEW = "interview"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class OnboardingStatus(str, enum.Enum):
    """Status of employee onboarding"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Candidate(Base):
    """Model for job candidates"""
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50))
    resume_text = Column(Text)
    resume_file_path = Column(String(500))
    
    # AI Analysis Results
    skills = Column(JSON)  # Extracted skills
    experience_years = Column(Integer)
    ai_summary = Column(Text)  # AI-generated summary
    match_score = Column(Integer)  # 0-100 score
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = relationship("JobApplication", back_populates="candidate")


class JobPosition(Base):
    """Model for job positions"""
    __tablename__ = "job_positions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(JSON)  # List of required skills
    experience_required = Column(Integer)  # Years of experience
    department = Column(String(100))
    salary_range = Column(String(100))  # Salary range (e.g., "$80k-$120k")
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = relationship("JobApplication", back_populates="position")


class JobApplication(Base):
    """Model for job applications"""
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("job_positions.id"), nullable=False)
    
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.SUBMITTED)
    
    # AI Agent Analysis
    screening_notes = Column(Text)  # AI-generated screening notes
    strengths = Column(JSON)  # List of strengths
    concerns = Column(JSON)  # List of concerns
    recommendation = Column(String(50))  # recommend/review/reject
    
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="applications")
    position = relationship("JobPosition", back_populates="applications")


class Employee(Base):
    """Model for employees"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=True)
    employee_id = Column(String(50), unique=True, nullable=False)
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50))
    position = Column(String(255))
    department = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    hire_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    onboarding = relationship("OnboardingProcess", back_populates="employee", uselist=False)


class OnboardingProcess(Base):
    """Model for employee onboarding process"""
    __tablename__ = "onboarding_processes"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True)
    
    status = Column(SQLEnum(OnboardingStatus), default=OnboardingStatus.PENDING)
    
    # Onboarding Tasks
    checklist = Column(JSON)  # List of onboarding tasks
    completed_tasks = Column(JSON)  # List of completed task IDs
    
    # AI Agent Interactions
    interaction_history = Column(JSON)  # Chat history with onboarding agent
    documents_generated = Column(JSON)  # List of generated documents
    next_steps = Column(Text)  # AI-suggested next steps
    
    start_date = Column(DateTime)
    completion_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="onboarding")
