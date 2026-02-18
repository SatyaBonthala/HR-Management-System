"""
Seed the database with sample data for testing
Run this after init_db.py to populate the system with test data
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import JobPosition, Candidate, Employee, Base
from datetime import datetime

def seed_job_positions(db: Session):
    """Create sample job positions"""
    positions = [
        {
            "title": "Senior Python Developer",
            "description": """We're seeking an experienced Python developer to join our engineering team. 
            The ideal candidate will have strong experience with FastAPI, microservices, and cloud technologies.
            You'll be responsible for designing and implementing backend services, mentoring junior developers,
            and contributing to architectural decisions.""",
            "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "Redis"],
            "experience_required": 5,
            "department": "Engineering",
            "is_active": True
        },
        {
            "title": "DevOps Engineer",
            "description": """Looking for a talented DevOps engineer to help us scale our infrastructure.
            You'll work on CI/CD pipelines, container orchestration, and cloud infrastructure automation.
            Experience with Kubernetes and Terraform is a must.""",
            "required_skills": ["Kubernetes", "Docker", "Terraform", "AWS", "CI/CD", "Python"],
            "experience_required": 4,
            "department": "Infrastructure",
            "is_active": True
        },
        {
            "title": "Frontend Developer",
            "description": """Join our product team as a frontend developer. You'll build responsive,
            intuitive user interfaces using React and modern web technologies. Strong CSS skills and
            an eye for design are essential.""",
            "required_skills": ["React", "TypeScript", "CSS", "HTML", "REST APIs", "Git"],
            "experience_required": 3,
            "department": "Product",
            "is_active": True
        },
        {
            "title": "Data Scientist",
            "description": """We're looking for a data scientist to help us derive insights from our data.
            You'll work on machine learning models, data analysis, and visualization. Experience with
            Python, pandas, and scikit-learn is required.""",
            "required_skills": ["Python", "Pandas", "Scikit-learn", "SQL", "Machine Learning", "Statistics"],
            "experience_required": 3,
            "department": "Data",
            "is_active": True
        },
        {
            "title": "Product Manager",
            "description": """Seeking an experienced product manager to lead our product initiatives.
            You'll work closely with engineering, design, and business teams to define and execute
            product strategy. Strong technical background preferred.""",
            "required_skills": ["Product Strategy", "Agile", "User Research", "Analytics", "Communication"],
            "experience_required": 6,
            "department": "Product",
            "is_active": True
        }
    ]
    
    created_positions = []
    for pos_data in positions:
        position = JobPosition(**pos_data)
        db.add(position)
        created_positions.append(position)
    
    db.commit()
    for pos in created_positions:
        db.refresh(pos)
    
    print(f"✓ Created {len(created_positions)} job positions")
    return created_positions

def seed_candidates(db: Session):
    """Create sample candidates"""
    candidates = [
        {
            "name": "Alice Chen",
            "email": "alice.chen@email.com",
            "phone": "+1-555-0101",
            "resume_text": """
            Alice Chen
            Senior Software Engineer
            
            PROFESSIONAL SUMMARY:
            Highly skilled software engineer with 7 years of experience in backend development.
            Expert in Python, microservices architecture, and cloud technologies. Proven track
            record of leading teams and delivering scalable solutions.
            
            TECHNICAL SKILLS:
            • Languages: Python, Go, JavaScript
            • Frameworks: FastAPI, Django, Flask
            • Databases: PostgreSQL, Redis, MongoDB
            • Cloud & DevOps: AWS (EC2, Lambda, RDS, S3), Docker, Kubernetes
            • Tools: Git, Jenkins, Terraform
            
            PROFESSIONAL EXPERIENCE:
            
            Senior Software Engineer | TechCorp Inc. | 2020 - Present
            • Led development of microservices platform serving 2M+ users
            • Designed and implemented RESTful APIs using FastAPI
            • Reduced infrastructure costs by 45% through optimization
            • Mentored 3 junior developers
            
            Software Engineer | StartupXYZ | 2018 - 2020
            • Built backend services using Python and Django
            • Implemented caching strategies with Redis
            • Collaborated with frontend team on API design
            
            Junior Developer | WebSolutions | 2017 - 2018
            • Developed web applications using Python and Flask
            • Wrote unit and integration tests
            • Participated in code reviews
            
            EDUCATION:
            B.S. Computer Science | State University | 2017
            """
        },
        {
            "name": "Bob Martinez",
            "email": "bob.martinez@email.com",
            "phone": "+1-555-0102",
            "resume_text": """
            Bob Martinez
            DevOps Engineer
            
            SUMMARY:
            Experienced DevOps engineer with 5 years of experience in cloud infrastructure,
            CI/CD, and container orchestration. Passionate about automation and scalability.
            
            SKILLS:
            • Container Orchestration: Kubernetes, Docker Swarm
            • Infrastructure as Code: Terraform, CloudFormation
            • Cloud Platforms: AWS, Azure
            • CI/CD: Jenkins, GitLab CI, GitHub Actions
            • Scripting: Python, Bash
            • Monitoring: Prometheus, Grafana, ELK Stack
            
            EXPERIENCE:
            
            DevOps Engineer | CloudTech Solutions | 2021 - Present
            • Managed Kubernetes clusters serving 500+ microservices
            • Implemented infrastructure as code using Terraform
            • Reduced deployment time by 60% with automated pipelines
            • Set up monitoring and alerting systems
            
            Systems Engineer | DataCorp | 2019 - 2021
            • Maintained AWS infrastructure for production systems
            • Automated server provisioning and configuration
            • Implemented backup and disaster recovery procedures
            
            CERTIFICATIONS:
            • AWS Certified Solutions Architect
            • Certified Kubernetes Administrator (CKA)
            """
        },
        {
            "name": "Carol Patel",
            "email": "carol.patel@email.com",
            "phone": "+1-555-0103",
            "resume_text": """
            Carol Patel
            Frontend Developer
            
            ABOUT ME:
            Creative frontend developer with 4 years of experience building beautiful,
            responsive web applications. Strong focus on user experience and performance.
            
            TECHNICAL SKILLS:
            • Frontend: React, Vue.js, TypeScript, JavaScript (ES6+)
            • Styling: CSS3, SASS, Tailwind CSS, Material-UI
            • State Management: Redux, Context API, Vuex
            • Testing: Jest, React Testing Library, Cypress
            • Build Tools: Webpack, Vite, npm
            • Design: Figma, Adobe XD
            
            WORK HISTORY:
            
            Senior Frontend Developer | UX Innovations | 2022 - Present
            • Led frontend development for SaaS product with 50k users
            • Implemented responsive design system using React and Tailwind
            • Improved page load time by 40% through optimization
            • Collaborated with designers on UI/UX improvements
            
            Frontend Developer | WebApps Co | 2020 - 2022
            • Built interactive dashboards using React and D3.js
            • Integrated REST APIs and WebSocket connections
            • Wrote comprehensive unit and integration tests
            
            EDUCATION:
            B.A. Computer Science | Tech University | 2020
            """
        },
        {
            "name": "David Kim",
            "email": "david.kim@email.com",
            "phone": "+1-555-0104",
            "resume_text": """
            David Kim
            Data Scientist
            
            PROFILE:
            Data scientist with 4 years of experience in machine learning, statistical analysis,
            and data visualization. Skilled at turning data into actionable insights.
            
            EXPERTISE:
            • Machine Learning: Scikit-learn, TensorFlow, PyTorch
            • Data Analysis: Pandas, NumPy, SciPy
            • Visualization: Matplotlib, Seaborn, Plotly
            • Databases: SQL, PostgreSQL, MongoDB
            • Big Data: Spark, Hadoop
            • Languages: Python, R, SQL
            
            PROFESSIONAL EXPERIENCE:
            
            Data Scientist | Analytics Pro | 2021 - Present
            • Developed predictive models improving conversion rates by 25%
            • Built recommendation system serving 100k+ users
            • Created dashboards and visualizations for stakeholders
            • Conducted A/B testing and statistical analysis
            
            Junior Data Scientist | DataWorks | 2020 - 2021
            • Performed exploratory data analysis on large datasets
            • Built classification and regression models
            • Collaborated with engineering team on model deployment
            
            EDUCATION:
            M.S. Data Science | University of Technology | 2020
            B.S. Mathematics | State College | 2018
            """
        }
    ]
    
    created_candidates = []
    for cand_data in candidates:
        candidate = Candidate(**cand_data)
        db.add(candidate)
        created_candidates.append(candidate)
    
    db.commit()
    for cand in created_candidates:
        db.refresh(cand)
    
    print(f"✓ Created {len(created_candidates)} candidates")
    return created_candidates

def seed_employees(db: Session):
    """Create sample employees"""
    employees = [
        {
            "employee_id": "EMP00001",
            "name": "Emma Thompson",
            "email": "emma.thompson@company.com",
            "phone": "+1-555-0201",
            "position": "Senior Python Developer",
            "department": "Engineering",
            "hire_date": datetime(2024, 1, 15)
        },
        {
            "employee_id": "EMP00002",
            "name": "Frank Wilson",
            "email": "frank.wilson@company.com",
            "phone": "+1-555-0202",
            "position": "DevOps Engineer",
            "department": "Infrastructure",
            "hire_date": datetime(2024, 2, 1)
        }
    ]
    
    created_employees = []
    for emp_data in employees:
        employee = Employee(**emp_data)
        db.add(employee)
        created_employees.append(employee)
    
    db.commit()
    for emp in created_employees:
        db.refresh(emp)
    
    print(f"✓ Created {len(created_employees)} employees")
    return created_employees

def main():
    """Seed the database with sample data"""
    print("\n" + "="*60)
    print("  Seeding Database with Sample Data")
    print("="*60 + "\n")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_positions = db.query(JobPosition).count()
        if existing_positions > 0:
            print(f"⚠️  Database already has {existing_positions} job positions.")
            response = input("Do you want to add more sample data? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return
        
        # Seed data
        print("\nAdding sample data...\n")
        positions = seed_job_positions(db)
        candidates = seed_candidates(db)
        employees = seed_employees(db)
        
        print("\n" + "="*60)
        print("  ✅ Database Seeding Complete!")
        print("="*60)
        print(f"\nSummary:")
        print(f"  • Job Positions: {len(positions)}")
        print(f"  • Candidates: {len(candidates)}")
        print(f"  • Employees: {len(employees)}")
        print(f"\nYou can now:")
        print(f"  1. Start the API: python main.py")
        print(f"  2. Run tests: python test_system.py")
        print(f"  3. Check API docs: http://localhost:8000/docs")
        print()
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
