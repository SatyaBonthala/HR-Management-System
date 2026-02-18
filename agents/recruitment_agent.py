"""
Recruitment Agent - AI-powered resume screening and candidate evaluation
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, List
from config import settings
import json
import re


class RecruitmentAgent:
    """AI Agent for screening resumes and evaluating candidates"""
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.RECRUITMENT_AGENT_MODEL,
            temperature=settings.AGENT_TEMPERATURE,
            max_tokens=settings.AGENT_MAX_TOKENS,
            api_key=settings.GROQ_API_KEY
        )
    
    def screen_candidate(self, resume_text: str, job_description: str, 
                        required_skills: List[str], experience_required: int) -> Dict:
        """
        Screen a candidate's resume against job requirements
        
        Args:
            resume_text: The candidate's resume text
            job_description: The job description
            required_skills: List of required skills
            experience_required: Years of experience required
            
        Returns:
            Dict with screening results including skills, summary, score, and recommendation
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an experienced technical recruiter with 15+ years of experience 
            in talent acquisition. You analyze resumes thoroughly and provide data-driven hiring recommendations."""),
            ("human", """Analyze the following resume against the job requirements and provide a comprehensive evaluation.
            
JOB DESCRIPTION:
{job_description}

REQUIRED SKILLS:
{required_skills}

EXPERIENCE REQUIRED:
{experience_required} years

CANDIDATE RESUME:
{resume_text}

Please provide your analysis in the following format:

SKILLS:
List all technical and soft skills found in the resume (one per line, starting with -)

EXPERIENCE:
State the estimated years of relevant experience (just the number)

SUMMARY:
Provide a 2-3 sentence summary of the candidate's background

MATCH SCORE:
Provide a score from 0-100 based on how well the candidate fits the requirements

STRENGTHS:
List 3-5 key strengths (one per line, starting with -)

CONCERNS:
List 2-4 potential concerns or gaps (one per line, starting with -)

RECOMMENDATION:
State one of: recommend, review, or reject
With a brief justification (1-2 sentences)""")
        ])
        
        chain = prompt | self.llm
        
        result = chain.invoke({
            "job_description": job_description,
            "required_skills": ", ".join(required_skills),
            "experience_required": experience_required,
            "resume_text": resume_text
        })
        
        # Parse the result
        parsed_result = self._parse_screening_result(result.content)
        
        return parsed_result
    
    def _parse_screening_result(self, result_text: str) -> Dict:
        """
        Parse the AI agent's response into structured data
        
        This is a simplified parser. In production, you might want to use
        more structured output formats or JSON parsing.
        """
        import re
        
        # Default structure
        parsed = {
            "skills": [],
            "experience_years": 0,
            "ai_summary": "",
            "match_score": 50,
            "strengths": [],
            "concerns": [],
            "recommendation": "review",
            "screening_notes": result_text
        }
        
        # Try to extract match score
        score_match = re.search(r'match\s*score[:\s]+(\d+)', result_text, re.IGNORECASE)
        if score_match:
            parsed["match_score"] = int(score_match.group(1))
        
        # Try to extract experience years
        exp_match = re.search(r'(\d+)\s*years?\s+(?:of\s+)?experience', result_text, re.IGNORECASE)
        if exp_match:
            parsed["experience_years"] = int(exp_match.group(1))
        
        # Try to extract recommendation
        if re.search(r'recommendation[:\s]+recommend', result_text, re.IGNORECASE):
            parsed["recommendation"] = "recommend"
        elif re.search(r'recommendation[:\s]+reject', result_text, re.IGNORECASE):
            parsed["recommendation"] = "reject"
        else:
            parsed["recommendation"] = "review"
        
        # Extract skills (look for common patterns)
        skills_section = re.search(r'skills[:\s]+(.*?)(?:\n\n|\nexperience|\nsummary|$)', 
                                  result_text, re.IGNORECASE | re.DOTALL)
        if skills_section:
            skills_text = skills_section.group(1)
            # Simple extraction: look for comma-separated or bullet-pointed items
            skills = re.findall(r'[-•*]\s*([^\n]+)', skills_text)
            if not skills:
                skills = [s.strip() for s in skills_text.split(',') if s.strip()]
            parsed["skills"] = skills[:15]  # Limit to 15 skills
        
        # Extract summary
        summary_match = re.search(r'summary[:\s]+(.*?)(?:\n\n|\nmatch|$)', 
                                 result_text, re.IGNORECASE | re.DOTALL)
        if summary_match:
            parsed["ai_summary"] = summary_match.group(1).strip()
        
        # Extract strengths
        strengths_match = re.search(r'strengths[:\s]+(.*?)(?:\n\n|\nconcerns|$)',
                                   result_text, re.IGNORECASE | re.DOTALL)
        if strengths_match:
            strengths = re.findall(r'[-•*]\s*([^\n]+)', strengths_match.group(1))
            parsed["strengths"] = strengths[:5]
        
        # Extract concerns
        concerns_match = re.search(r'concerns[:\s]+(.*?)(?:\n\n|\nrecommendation|$)',
                                  result_text, re.IGNORECASE | re.DOTALL)
        if concerns_match:
            concerns = re.findall(r'[-•*]\s*([^\n]+)', concerns_match.group(1))
            parsed["concerns"] = concerns[:5]
        
        return parsed
    
    def compare_candidates(self, candidates_data: List[Dict]) -> List[Dict]:
        """
        Compare multiple candidates and rank them
        
        Args:
            candidates_data: List of candidate data with their screening results
            
        Returns:
            Ranked list of candidates with comparative analysis
        """
        
        comparison_task = Task(
            description=f"""
            Compare the following candidates and provide a ranking based on their qualifications:
            
            {self._format_candidates_for_comparison(candidates_data)}
            
            Provide a ranking from best to least qualified, with brief justification for each rank.
            """,
            agent=self.recruiter,
            expected_output="Ranked list of candidates with justifications"
        )
        
        crew = Crew(
            agents=[self.recruiter],
            tasks=[comparison_task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {"comparison": str(result)}
    
    def _format_candidates_for_comparison(self, candidates_data: List[Dict]) -> str:
        """Format candidate data for comparison"""
        formatted = []
        for i, candidate in enumerate(candidates_data, 1):
            formatted.append(f"""
            Candidate {i}: {candidate.get('name', 'Unknown')}
            - Match Score: {candidate.get('match_score', 'N/A')}
            - Experience: {candidate.get('experience_years', 'N/A')} years
            - Key Skills: {', '.join(candidate.get('skills', [])[:5])}
            - Summary: {candidate.get('ai_summary', 'No summary available')}
            """)
        return '\n'.join(formatted)


# Singleton instance
recruitment_agent = RecruitmentAgent()
