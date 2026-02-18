# 🤖 Agentic HR Management System

An AI-powered HR management system that uses intelligent agents to automate recruitment screening and employee onboarding processes.

## ✨ Features

### 🎯 Recruitment Agent
- **Automated Resume Screening**: AI analyzes resumes and extracts key information
- **Skills Extraction**: Identifies technical and soft skills from resumes
- **Match Scoring**: Provides 0-100 match score against job requirements
- **Candidate Evaluation**: Generates comprehensive screening notes with strengths and concerns
- **Smart Recommendations**: Categorizes candidates as recommend/review/reject

### 👋 Onboarding Agent
- **Personalized Checklists**: Creates customized onboarding plans based on role and department
- **Interactive Chat**: Answer employee questions throughout onboarding
- **Progress Tracking**: Monitors completion of onboarding tasks
- **Document Generation**: Creates welcome emails, training plans, and other onboarding materials
- **Proactive Guidance**: Suggests next steps and provides encouragement

## 🏗️ Architecture

```
┌─────────────────┐
│   FastAPI App   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼────┐
│  AI  │  │  AI   │
│Recruit│  │Onboard│
│Agent │  │ Agent │
└───┬──┘  └──┬────┘
    │        │
    └────┬───┘
         │
    ┌────▼────────┐
    │ PostgreSQL  │
    └─────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- OpenAI API Key

### Installation

1. **Clone or navigate to the project directory**
```bash
cd "c:\Users\Satya Bonthala\Documents\Satya_Projects\HR management system"
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Set up PostgreSQL database**
```bash
# Create database
createdb hr_management

# Or using psql
psql -U postgres
CREATE DATABASE hr_management;
\q
```

6. **Configure environment variables**
```bash
# Copy example env file
copy .env.example .env

# Edit .env file with your settings:
# - DATABASE_URL: Your PostgreSQL connection string
# - OPENAI_API_KEY: Your OpenAI API key
```

7. **Initialize the database**
```bash
python init_db.py
```

8. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## 📚 API Endpoints

### Job Positions
- `POST /api/positions` - Create a job position
- `GET /api/positions` - List all positions
- `GET /api/positions/{id}` - Get specific position

### Candidates & Applications
- `POST /api/candidates` - Add a new candidate
- `GET /api/candidates` - List all candidates
- `POST /api/applications` - Submit application (triggers AI screening)
- `GET /api/applications` - List applications with filters

### Employees & Onboarding
- `POST /api/employees` - Create employee (initializes onboarding)
- `GET /api/employees` - List employees
- `GET /api/onboarding/{employee_id}` - Get onboarding status
- `POST /api/onboarding/chat` - Chat with onboarding agent
- `POST /api/onboarding/{employee_id}/complete-task` - Mark task complete

### Analytics
- `GET /api/analytics/recruitment` - Recruitment statistics
- `GET /api/analytics/onboarding` - Onboarding statistics

## 🎮 Usage Examples

### 1. Create a Job Position
```bash
curl -X POST "http://localhost:8000/api/positions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer...",
    "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
    "experience_required": 5,
    "department": "Engineering"
  }'
```

### 2. Add a Candidate and Apply
```bash
# Create candidate
curl -X POST "http://localhost:8000/api/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "resume_text": "Experienced Python developer with 6 years..."
  }'

# Submit application (AI screening happens automatically)
curl -X POST "http://localhost:8000/api/applications" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "position_id": 1
  }'
```

### 3. Create Employee and Start Onboarding
```bash
# Create employee
curl -X POST "http://localhost:8000/api/employees" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@company.com",
    "phone": "+1234567890",
    "position": "Senior Python Developer",
    "department": "Engineering"
  }'

# Chat with onboarding agent
curl -X POST "http://localhost:8000/api/onboarding/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "message": "What should I do on my first day?"
  }'
```

## 🧪 Testing the System

### Test Recruitment Agent
1. Create a job position via the API
2. Add a candidate with resume text
3. Submit an application
4. Wait a few seconds for AI screening
5. Check the application to see AI-generated analysis

### Test Onboarding Agent
1. Create a new employee
2. Wait for onboarding initialization
3. Check onboarding status to see the checklist
4. Use the chat endpoint to ask questions
5. Mark tasks as completed

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `RECRUITMENT_AGENT_MODEL`: GPT model for recruitment (default: gpt-4-turbo-preview)
- `ONBOARDING_AGENT_MODEL`: GPT model for onboarding (default: gpt-4-turbo-preview)
- `AGENT_TEMPERATURE`: Temperature for AI responses (default: 0.7)
- `AGENT_MAX_TOKENS`: Max tokens per response (default: 2000)

### Database Schema
The application uses SQLAlchemy ORM with the following main models:
- `Candidate`: Job candidates with AI-extracted information
- `JobPosition`: Available positions
- `JobApplication`: Applications with AI screening results
- `Employee`: Hired employees
- `OnboardingProcess`: Onboarding progress and chat history

## 🎯 Key Features Explained

### AI Recruitment Agent
The recruitment agent:
1. Analyzes resume text against job requirements
2. Extracts skills and experience
3. Generates a match score (0-100)
4. Lists strengths and concerns
5. Provides a recommendation (recommend/review/reject)
6. All processing happens asynchronously

### AI Onboarding Agent
The onboarding agent:
1. Creates personalized onboarding checklists
2. Answers employee questions in real-time
3. Tracks progress and provides encouragement
4. Generates onboarding documents
5. Suggests next steps proactively

## 📊 Project Structure

```
HR management system/
├── agents/
│   ├── __init__.py
│   ├── recruitment_agent.py    # AI recruitment agent
│   └── onboarding_agent.py     # AI onboarding agent
├── config.py                   # Configuration settings
├── database.py                 # Database setup
├── models.py                   # SQLAlchemy models
├── schemas.py                  # Pydantic schemas
├── main.py                     # FastAPI application
├── init_db.py                  # Database initialization
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
└── README.md                  # This file
```

## 🚧 Development Roadmap

### Phase 1 (Current - MVP)
- ✅ Recruitment agent with resume screening
- ✅ Onboarding agent with interactive chat
- ✅ Basic CRUD operations
- ✅ RESTful API with FastAPI

### Phase 2 (Next Steps)
- [ ] File upload for resumes (PDF, DOCX)
- [ ] Email notifications
- [ ] Calendar integration for interviews
- [ ] Authentication & authorization
- [ ] Role-based access control (RBAC)

### Phase 3 (Future)
- [ ] Frontend dashboard (React/Vue)
- [ ] Advanced analytics and reporting
- [ ] Performance review agent
- [ ] Leave management agent
- [ ] Integration with Slack/Teams
- [ ] Document storage (S3/Azure Blob)

## 🛠️ Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready

# Verify connection string in .env
echo $DATABASE_URL
```

### OpenAI API Issues
- Ensure your API key is valid and has credits
- Check rate limits on your OpenAI account
- Verify the model name is correct (gpt-4-turbo-preview, gpt-3.5-turbo, etc.)

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome!

## 📧 Contact

For questions or issues, please create an issue in the repository.

---

**Built with ❤️ using FastAPI, LangChain, and CrewAI**
