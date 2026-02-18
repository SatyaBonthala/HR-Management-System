"""
Onboarding Agent - AI-powered employee onboarding assistant
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, List, Optional
from config import settings
from datetime import datetime


class OnboardingAgent:
    """AI Agent for guiding new employees through the onboarding process"""
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.ONBOARDING_AGENT_MODEL,
            temperature=settings.AGENT_TEMPERATURE,
            max_tokens=settings.AGENT_MAX_TOKENS,
            api_key=settings.GROQ_API_KEY
        )
    
    def create_onboarding_checklist(self, employee_data: Dict) -> Dict:
        """
        Create a personalized onboarding checklist for a new employee
        
        Args:
            employee_data: Dictionary containing employee information
                (name, position, department, hire_date, etc.)
                
        Returns:
            Dict with onboarding checklist and timeline
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an experienced HR onboarding specialist who creates 
            comprehensive and personalized onboarding plans for new employees."""),
            ("human", """Create a comprehensive onboarding checklist for a new employee with the following details:

Name: {name}
Position: {position}
Department: {department}
Start Date: {hire_date}

Create a detailed onboarding checklist that includes:
1. Pre-arrival tasks (before first day)
2. First day activities
3. First week tasks
4. First month milestones
5. Department-specific requirements for {department}
6. Position-specific training for {position}

Each task should include:
- Task name
- Description
- Estimated time to complete
- Priority level (high/medium/low)

Also provide a welcome message and initial next steps.""")
        ])
        
        chain = prompt | self.llm
        
        result = chain.invoke({
            "name": employee_data.get('name', 'New Employee'),
            "position": employee_data.get('position', 'Not specified'),
            "department": employee_data.get('department', 'Not specified'),
            "hire_date": employee_data.get('hire_date', 'Not specified')
        })
        
        parsed_result = self._parse_checklist(result.content, employee_data)
        
        return parsed_result
    
    def handle_onboarding_query(self, employee_data: Dict, message: str, 
                               conversation_history: Optional[List[Dict]] = None) -> Dict:
        """
        Handle an employee's onboarding question or message
        
        Args:
            employee_data: Employee information
            message: The employee's message/question
            conversation_history: Previous conversation messages
            
        Returns:
            Dict with response and any action items
        """
        
        history_context = ""
        if conversation_history:
            history_context = "\n\nPrevious conversation:\n" + "\n".join([
                f"{'Employee' if msg.get('role') == 'employee' else 'Agent'}: {msg.get('content', '')}"
                for msg in conversation_history[-5:]  # Last 5 messages for context
            ])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a friendly and helpful HR onboarding assistant. 
            Your goal is to make new employees feel welcomed and supported during their onboarding journey."""),
            ("human", """You are assisting {name} who is onboarding as a {position} in the {department}.

{history_context}

The employee's current message:
"{message}"

Please provide:
1. A helpful, friendly, and comprehensive response to their query
2. Any relevant action items or next steps
3. Suggestions for related topics they might need to know about
4. If they're asking about a task, provide clear step-by-step guidance

Be warm, welcoming, and ensure they feel supported during their onboarding.""")
        ])
        
        chain = prompt | self.llm
        
        result = chain.invoke({
            "name": employee_data.get('name', 'an employee'),
            "position": employee_data.get('position', 'team member'),
            "department": employee_data.get('department', 'department'),
            "message": message,
            "history_context": history_context
        })
        
        return {
            "response": result.content,
            "timestamp": datetime.utcnow().isoformat(),
            "employee_message": message
        }
    
    def generate_onboarding_documents(self, employee_data: Dict, 
                                     document_types: List[str]) -> Dict:
        """
        Generate onboarding documents for an employee
        
        Args:
            employee_data: Employee information
            document_types: List of document types to generate 
                (e.g., ['welcome_email', 'first_day_agenda', 'training_plan'])
                
        Returns:
            Dict with generated documents
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert HR professional who creates professional, 
            personalized onboarding documents for new employees."""),
            ("human", """Generate the following onboarding documents for:

Name: {name}
Position: {position}
Department: {department}
Start Date: {hire_date}

Documents to generate:
{document_types}

For each document:
1. Create professional, personalized content
2. Include all relevant details
3. Maintain a warm, welcoming tone
4. Ensure clarity and actionable information

Format each document clearly with appropriate sections and structure.""")
        ])
        
        chain = prompt | self.llm
        
        result = chain.invoke({
            "name": employee_data.get('name', 'Employee'),
            "position": employee_data.get('position', 'Position'),
            "department": employee_data.get('department', 'Department'),
            "hire_date": employee_data.get('hire_date', 'Start Date'),
            "document_types": ', '.join(document_types)
        })
        
        return {
            "documents": self._parse_documents(result.content, document_types),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def update_onboarding_progress(self, employee_data: Dict, 
                                  completed_tasks: List[str],
                                  total_tasks: int) -> Dict:
        """
        Analyze onboarding progress and provide recommendations
        
        Args:
            employee_data: Employee information
            completed_tasks: List of completed task names
            total_tasks: Total number of tasks in checklist
            
        Returns:
            Dict with progress analysis and next steps
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a supportive HR onboarding specialist who monitors 
            employee progress and provides encouraging feedback and guidance."""),
            ("human", """Analyze the onboarding progress for {name}:

Position: {position}
Start Date: {hire_date}

Completed Tasks ({completed_count}/{total_tasks}):
{completed_tasks}

Please provide:
1. Overall progress assessment (on track / needs attention / excellent progress)
2. Congratulations on what they've accomplished
3. Top 3-5 priority tasks to focus on next
4. Any concerns or areas that need attention
5. Motivational message and encouragement

Be positive and supportive while ensuring they stay on track.""")
        ])
        
        chain = prompt | self.llm
        
        result = chain.invoke({
            "name": employee_data.get('name', 'the employee'),
            "position": employee_data.get('position', 'Not specified'),
            "hire_date": employee_data.get('hire_date', 'Not specified'),
            "completed_count": len(completed_tasks),
            "total_tasks": total_tasks,
            "completed_tasks": ', '.join(completed_tasks) if completed_tasks else 'None yet'
        })
        
        completion_percentage = (len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "progress_analysis": result.content,
            "completion_percentage": round(completion_percentage, 1),
            "completed_count": len(completed_tasks),
            "total_count": total_tasks,
            "status": "on_track" if completion_percentage >= 70 else "needs_attention"
        }
    
    def _parse_checklist(self, result_text: str, employee_data: Dict) -> Dict:
        """Parse the checklist from AI response"""
        import re
        
        # Simple parsing - extract tasks
        tasks = []
        task_matches = re.finditer(r'[-•*]\s*([^\n]+)', result_text)
        
        for idx, match in enumerate(task_matches):
            task_text = match.group(1).strip()
            if len(task_text) > 10:  # Filter out very short items
                tasks.append({
                    "id": f"task_{idx + 1}",
                    "name": task_text[:100],  # Limit length
                    "completed": False,
                    "priority": "medium"
                })
        
        # If no tasks found, create default ones
        if not tasks:
            tasks = [
                {"id": "task_1", "name": "Complete new hire paperwork", "completed": False, "priority": "high"},
                {"id": "task_2", "name": "Set up workstation and accounts", "completed": False, "priority": "high"},
                {"id": "task_3", "name": "Meet with direct manager", "completed": False, "priority": "high"},
                {"id": "task_4", "name": "Complete company orientation", "completed": False, "priority": "medium"},
                {"id": "task_5", "name": "Review employee handbook", "completed": False, "priority": "medium"},
            ]
        
        return {
            "checklist": tasks[:20],  # Limit to 20 tasks
            "full_response": result_text,
            "next_steps": "Start with high-priority tasks and reach out if you have any questions!",
            "created_at": datetime.utcnow().isoformat()
        }
    
    def _parse_documents(self, result_text: str, document_types: List[str]) -> Dict:
        """Parse generated documents from AI response"""
        # Simple split-based parsing
        documents = {}
        
        for doc_type in document_types:
            # Try to find section for this document type
            pattern = f"{doc_type}[:\n]+(.*?)(?=\n\n[A-Z]|$)"
            match = re.search(pattern, result_text, re.IGNORECASE | re.DOTALL)
            
            if match:
                documents[doc_type] = match.group(1).strip()
            else:
                documents[doc_type] = f"Document content for {doc_type}\n\n{result_text[:500]}..."
        
        return documents


# Singleton instance
onboarding_agent = OnboardingAgent()
