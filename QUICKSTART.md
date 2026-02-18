# Quick Start Guide - Agentic HR Management System

## 🎯 Goal
Get your HR system up and running in 10 minutes!

## 📋 Prerequisites Checklist
- [ ] Python 3.9+ installed
- [ ] PostgreSQL installed and running
- [ ] OpenAI API key ready
- [ ] Command prompt/terminal open

## 🚀 Setup Steps

### Step 1: Set up Python Environment (2 min)
```bash
# Navigate to project folder
cd "c:\Users\Satya Bonthala\Documents\Satya_Projects\HR management system"

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Database (2 min)
```bash
# Option A: Create database via command
createdb hr_management

# Option B: Using psql
psql -U postgres
CREATE DATABASE hr_management;
\q
```

### Step 3: Configure Environment (2 min)
```bash
# Copy example file
copy .env.example .env

# Edit .env with your text editor and set:
# 1. DATABASE_URL (e.g., postgresql://postgres:password@localhost:5432/hr_management)
# 2. OPENAI_API_KEY (your API key)
```

### Step 4: Initialize Database (1 min)
```bash
python init_db.py
```

You should see:
```
Creating database tables...
✓ Database tables created successfully!
```

### Step 5: Start the Application (1 min)
```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Test the System (2 min)
Open a new terminal and run:
```bash
# Activate venv first
venv\Scripts\activate

# Run test suite
python test_system.py
```

## 🎉 Success!

If everything works, you should be able to:

1. **API Documentation**: http://localhost:8000/docs
2. **Health Check**: http://localhost:8000/health

## 🧪 Try It Out

### Test Recruitment Agent
```bash
# 1. Create a job position (copy-paste in terminal or use Postman)
curl -X POST http://localhost:8000/api/positions -H "Content-Type: application/json" -d "{\"title\": \"Python Developer\", \"description\": \"We need a Python expert\", \"required_skills\": [\"Python\", \"FastAPI\"], \"experience_required\": 3, \"department\": \"Engineering\"}"

# 2. Add a candidate
curl -X POST http://localhost:8000/api/candidates -H "Content-Type: application/json" -d "{\"name\": \"John Doe\", \"email\": \"john@test.com\", \"resume_text\": \"Experienced Python developer with 5 years of FastAPI experience\"}"

# 3. Submit application (AI screening happens automatically!)
curl -X POST http://localhost:8000/api/applications -H "Content-Type: application/json" -d "{\"candidate_id\": 1, \"position_id\": 1}"

# 4. Wait 10 seconds, then check results
curl http://localhost:8000/api/applications/1
```

### Test Onboarding Agent
```bash
# 1. Create an employee
curl -X POST http://localhost:8000/api/employees -H "Content-Type: application/json" -d "{\"name\": \"Jane Smith\", \"email\": \"jane@company.com\", \"position\": \"Python Developer\", \"department\": \"Engineering\"}"

# 2. Wait 10 seconds, then check onboarding
curl http://localhost:8000/api/onboarding/1

# 3. Chat with onboarding agent
curl -X POST http://localhost:8000/api/onboarding/chat -H "Content-Type: application/json" -d "{\"employee_id\": 1, \"message\": \"What should I do on my first day?\"}"
```

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
pg_isready

# If not running, start it:
# Windows: Check Services or pg_ctl start
# Linux: sudo systemctl start postgresql
# Mac: brew services start postgresql
```

### OpenAI API Error
- Check your API key in .env
- Ensure you have credits: https://platform.openai.com/usage
- Try a different model (gpt-3.5-turbo is cheaper)

### Import Errors
```bash
# Reinstall everything
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Change port in main.py (last line):
uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
```

## 📚 Next Steps

1. **Explore the API**: http://localhost:8000/docs
2. **Read full documentation**: README.md
3. **Run comprehensive tests**: python test_system.py
4. **Build a frontend**: Consider React, Vue, or even Streamlit
5. **Add more features**: Check the Development Roadmap in README.md

## 💡 Pro Tips

- Use the interactive API docs at `/docs` - it's easier than curl!
- Check logs if something fails - errors are usually descriptive
- Start simple: Test one endpoint at a time
- The AI agents are stateless - each request is independent

## 🆘 Need Help?

1. Check the full README.md for detailed info
2. Look at test_system.py for working examples
3. Review the API docs at http://localhost:8000/docs
4. Check the logs in the terminal where the app is running

---

**You're all set! Happy coding! 🚀**
