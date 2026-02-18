"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# Candidate Schemas
class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class CandidateCreate(CandidateBase):
    resume_text: Optional[str] = None


class CandidateResponse(CandidateBase):
    id: int
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    ai_summary: Optional[str] = None
    match_score: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Job Position Schemas
class JobPositionBase(BaseModel):
    title: str
    description: str
    required_skills: List[str]
    experience_required: int
    department: str
    salary_range: Optional[str] = None


class JobPositionCreate(JobPositionBase):
    pass


class JobPositionResponse(JobPositionBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Job Application Schemas
class JobApplicationCreate(BaseModel):
    candidate_id: int
    position_id: int


class AIScreeningResult(BaseModel):
    """Nested AI screening result"""
    match_score: Optional[int] = None
    summary: Optional[str] = None
    strengths: Optional[List[str]] = None
    concerns: Optional[List[str]] = None
    recommendation: Optional[str] = None


class JobApplicationResponse(BaseModel):
    id: int
    candidate_id: int
    position_id: int
    status: str
    screening_notes: Optional[str] = None
    strengths: Optional[List[str]] = None
    concerns: Optional[List[str]] = None
    recommendation: Optional[str] = None
    applied_at: datetime
    ai_screening: Optional[AIScreeningResult] = None
    
    @property
    def _ai_screening(self):
        """Computed property for nested AI screening data"""
        if self.screening_notes or self.strengths or self.concerns or self.recommendation:
            return {
                "match_score": 0,  # Will be populated from candidate
                "summary": self.screening_notes or "",
                "strengths": self.strengths or [],
                "concerns": self.concerns or [],
                "recommendation": self.recommendation or "review"
            }
        return None
    
    class Config:
        from_attributes = True


# Employee Schemas
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    position: str
    department: str
    candidate_id: Optional[int] = None


class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    name: str
    email: str
    position: str
    department: str
    hire_date: datetime
    
    class Config:
        from_attributes = True


# Onboarding Schemas
class OnboardingMessage(BaseModel):
    employee_id: int
    message: str


class OnboardingResponse(BaseModel):
    id: int
    employee_id: int
    status: str
    checklist: Optional[List[dict]] = None
    completed_tasks: Optional[List[str]] = None
    next_steps: Optional[str] = None
    
    class Config:
        from_attributes = True


class OnboardingChatResponse(BaseModel):
    response: str
    updated_status: str
    next_steps: Optional[str] = None
