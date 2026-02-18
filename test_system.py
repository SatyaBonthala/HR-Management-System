"""
Test script to verify the system works
"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health_check():
    """Test if API is running"""
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_create_position():
    """Test creating a job position"""
    print_section("2. Create Job Position")
    
    position_data = {
        "title": "Senior Python Developer",
        "description": "We're looking for an experienced Python developer with expertise in FastAPI, microservices, and cloud technologies. The ideal candidate will lead backend development initiatives.",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
        "experience_required": 5,
        "department": "Engineering"
    }
    
    response = requests.post(f"{BASE_URL}/api/positions", json=position_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        position = response.json()
        print(f"Created Position ID: {position['id']}")
        print(f"Title: {position['title']}")
        return position['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_create_candidate():
    """Test creating a candidate"""
    print_section("3. Create Candidate")
    
    candidate_data = {
        "name": "Alex Johnson",
        "email": "alex.johnson@email.com",
        "phone": "+1-555-0123",
        "resume_text": """
        Alex Johnson
        Senior Software Engineer
        
        SUMMARY:
        Experienced software engineer with 7 years of experience in backend development.
        Expert in Python, FastAPI, and cloud technologies. Led multiple teams in developing
        scalable microservices architectures.
        
        SKILLS:
        - Programming: Python, JavaScript, Go
        - Frameworks: FastAPI, Django, Flask
        - Databases: PostgreSQL, MongoDB, Redis
        - Cloud: AWS (EC2, Lambda, RDS), Docker, Kubernetes
        - Tools: Git, CI/CD, Jenkins
        
        EXPERIENCE:
        Senior Software Engineer at TechCorp (2020-Present)
        - Led development of microservices platform serving 1M+ users
        - Implemented FastAPI-based REST APIs
        - Reduced infrastructure costs by 40% through optimization
        
        Software Engineer at StartupXYZ (2018-2020)
        - Built backend services using Python and Django
        - Worked with PostgreSQL and Redis for data management
        """
    }
    
    response = requests.post(f"{BASE_URL}/api/candidates", json=candidate_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        candidate = response.json()
        print(f"Created Candidate ID: {candidate['id']}")
        print(f"Name: {candidate['name']}")
        return candidate['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_create_application(candidate_id, position_id):
    """Test creating an application (triggers AI screening)"""
    print_section("4. Submit Application (AI Screening)")
    
    application_data = {
        "candidate_id": candidate_id,
        "position_id": position_id
    }
    
    response = requests.post(f"{BASE_URL}/api/applications", json=application_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        application = response.json()
        print(f"Created Application ID: {application['id']}")
        print(f"Status: {application['status']}")
        print("\nAI Screening initiated in background...")
        print("Waiting 10 seconds for AI processing...")
        sleep(10)
        return application['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_check_screening(application_id):
    """Check the AI screening results"""
    print_section("5. Check AI Screening Results")
    
    response = requests.get(f"{BASE_URL}/api/applications/{application_id}")
    if response.status_code == 200:
        application = response.json()
        print(f"\nApplication Status: {application['status']}")
        print(f"Recommendation: {application.get('recommendation', 'Processing...')}")
        
        if application.get('screening_notes'):
            print(f"\n📋 Screening Notes:")
            print(application['screening_notes'][:500] + "...")
        
        if application.get('strengths'):
            print(f"\n✅ Strengths:")
            for strength in application['strengths']:
                print(f"  • {strength}")
        
        if application.get('concerns'):
            print(f"\n⚠️  Concerns:")
            for concern in application['concerns']:
                print(f"  • {concern}")
        
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_create_employee():
    """Test creating an employee (triggers onboarding)"""
    print_section("6. Create Employee (Onboarding)")
    
    employee_data = {
        "name": "Sarah Williams",
        "email": "sarah.williams@company.com",
        "phone": "+1-555-0456",
        "position": "Senior Python Developer",
        "department": "Engineering"
    }
    
    response = requests.post(f"{BASE_URL}/api/employees", json=employee_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        employee = response.json()
        print(f"Created Employee ID: {employee['id']}")
        print(f"Employee Number: {employee['employee_id']}")
        print(f"Name: {employee['name']}")
        print("\nOnboarding initialization started in background...")
        print("Waiting 10 seconds for AI processing...")
        sleep(10)
        return employee['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_check_onboarding(employee_id):
    """Check onboarding status"""
    print_section("7. Check Onboarding Status")
    
    response = requests.get(f"{BASE_URL}/api/onboarding/{employee_id}")
    if response.status_code == 200:
        onboarding = response.json()
        print(f"\nOnboarding Status: {onboarding['status']}")
        
        if onboarding.get('checklist'):
            print(f"\n📝 Onboarding Checklist ({len(onboarding['checklist'])} tasks):")
            for i, task in enumerate(onboarding['checklist'][:5], 1):
                status = "✓" if task.get('completed') else "○"
                print(f"  {status} {task.get('name', 'Task')}")
            if len(onboarding['checklist']) > 5:
                print(f"  ... and {len(onboarding['checklist']) - 5} more tasks")
        
        if onboarding.get('next_steps'):
            print(f"\n🎯 Next Steps:")
            print(f"  {onboarding['next_steps']}")
        
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_onboarding_chat(employee_id):
    """Test chatting with onboarding agent"""
    print_section("8. Chat with Onboarding Agent")
    
    chat_data = {
        "employee_id": employee_id,
        "message": "What should I do on my first day? I'm excited but a bit nervous!"
    }
    
    print(f"\n💬 Employee: {chat_data['message']}")
    
    response = requests.post(f"{BASE_URL}/api/onboarding/chat", json=chat_data)
    if response.status_code == 200:
        chat_response = response.json()
        print(f"\n🤖 Onboarding Agent:")
        print(f"  {chat_response['response'][:500]}...")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_analytics():
    """Test analytics endpoints"""
    print_section("9. Analytics")
    
    # Recruitment analytics
    response = requests.get(f"{BASE_URL}/api/analytics/recruitment")
    if response.status_code == 200:
        analytics = response.json()
        print("\n📊 Recruitment Analytics:")
        print(f"  Total Positions: {analytics['total_positions']}")
        print(f"  Active Positions: {analytics['active_positions']}")
        print(f"  Total Candidates: {analytics['total_candidates']}")
        print(f"  Total Applications: {analytics['total_applications']}")
    
    # Onboarding analytics
    response = requests.get(f"{BASE_URL}/api/analytics/onboarding")
    if response.status_code == 200:
        analytics = response.json()
        print("\n📊 Onboarding Analytics:")
        print(f"  Total Employees: {analytics['total_employees']}")
        print(f"  Active Onboarding: {analytics['total_onboarding']}")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  🤖 Agentic HR Management System - Test Suite")
    print("="*60)
    print("\nMake sure the API is running at http://localhost:8000")
    print("Press Enter to continue or Ctrl+C to cancel...")
    input()
    
    try:
        # Test health
        if not test_health_check():
            print("\n❌ API is not running. Start it with: python main.py")
            return
        
        # Test recruitment flow
        position_id = test_create_position()
        if not position_id:
            print("\n⚠️  Failed to create position")
            return
        
        candidate_id = test_create_candidate()
        if not candidate_id:
            print("\n⚠️  Failed to create candidate")
            return
        
        application_id = test_create_application(candidate_id, position_id)
        if application_id:
            test_check_screening(application_id)
        
        # Test onboarding flow
        employee_id = test_create_employee()
        if employee_id:
            test_check_onboarding(employee_id)
            test_onboarding_chat(employee_id)
        
        # Test analytics
        test_analytics()
        
        print_section("✅ All Tests Completed!")
        print("\nCheck the API docs at: http://localhost:8000/docs")
        
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
