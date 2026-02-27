# 📋 Pre-Deployment Checklist

Complete these steps before deploying your HR Management System.

## 🔐 Security & Configuration

- [ ] **Environment Variables**
  - [ ] All sensitive data moved to environment variables (no hardcoded keys)
  - [ ] `.env` file added to `.gitignore`
  - [ ] Created `.env.example` files as templates
  
- [ ] **API Keys**
  - [ ] Obtained Groq API key from [console.groq.com](https://console.groq.com)
  - [ ] API key tested locally
  - [ ] API key has sufficient credits/quota
  
- [ ] **Secret Key**
  - [ ] Generated secure SECRET_KEY for production
  - [ ] Command: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

## 📦 Code Preparation

- [ ] **Dependencies**
  - [ ] All dependencies listed in `requirements.txt`
  - [ ] Frontend dependencies in `frontend/package.json`
  - [ ] Tested with: `pip install -r requirements.txt`
  
- [ ] **Database**
  - [ ] Database schema is finalized
  - [ ] Migration scripts ready (`init_db.py`)
  - [ ] Seed data prepared (optional)
  
- [ ] **CORS Configuration**
  - [ ] CORS origins updated in `main.py` for production domains
  - [ ] Example:
    ```python
    allow_origins=[
        "http://localhost:5173",
        "https://your-frontend-domain.com",
    ]
    ```

## 🧪 Testing

- [ ] **Local Testing**
  - [ ] Backend runs successfully: `uvicorn main:app --reload`
  - [ ] Frontend builds successfully: `cd frontend && npm run build`
  - [ ] All API endpoints working
  - [ ] Database operations working
  - [ ] AI agents responding correctly
  
- [ ] **Integration Testing**
  - [ ] Frontend connects to backend
  - [ ] Create/read/update operations work
  - [ ] Recruitment agent screens candidates
  - [ ] Onboarding agent generates checklists

## 📝 Repository Setup

- [ ] **Git Repository**
  - [ ] Git initialized: `git init`
  - [ ] All changes committed: `git add . && git commit -m "Ready for deployment"`
  - [ ] GitHub repository created
  - [ ] Code pushed to GitHub: `git push origin main`
  
- [ ] **`.gitignore` File**
  - [ ] `.env` files excluded
  - [ ] `__pycache__/` excluded
  - [ ] `node_modules/` excluded
  - [ ] Database files excluded (if any)
  - [ ] `*.pyc` excluded

## 🗄️ Database Service Selection

Choose one database hosting service:

- [ ] **Neon** (neon.tech) - Recommended
  - [ ] Account created
  - [ ] Project created
  - [ ] Connection string copied
  
- [ ] **Supabase** (supabase.com)
  - [ ] Project created
  - [ ] PostgreSQL connection string obtained
  
- [ ] **Railway** (railway.app) - If deploying full app there
  - [ ] PostgreSQL service added
  
- [ ] **Render** (render.com)
  - [ ] PostgreSQL database created

## 🚀 Deployment Platform Selection

Choose your deployment strategy:

### Option 1: Vercel
- [ ] Vercel account created (vercel.com)
- [ ] GitHub connected to Vercel
- [ ] Understand serverless limitations (10s timeout on free tier)

### Option 2: Railway
- [ ] Railway account created (railway.app)
- [ ] GitHub connected to Railway
- [ ] $5/month free credit is available

### Option 3: Render
- [ ] Render account created (render.com)
- [ ] GitHub connected to Render
- [ ] True free tier (no credit card for 90 days)

### Option 4: VPS (Advanced)
- [ ] VPS created (DigitalOcean, AWS, etc.)
- [ ] SSH access configured
- [ ] Docker installed
- [ ] Domain name configured (optional)

## 🔧 Configuration Files

- [ ] **Backend Configuration**
  - [ ] `vercel.json` configured (if using Vercel)
  - [ ] `Dockerfile` present and tested
  - [ ] `docker-compose.yml` configured
  
- [ ] **Frontend Configuration**
  - [ ] `vite.config.js` configured
  - [ ] Build process tested
  - [ ] API URL configuration ready for production

## 📊 Monitoring & Maintenance

- [ ] **Plan for Monitoring**
  - [ ] Know where to check logs for your platform
  - [ ] Error tracking strategy (optional: Sentry)
  - [ ] Uptime monitoring (optional: UptimeRobot)
  
- [ ] **Backup Strategy**
  - [ ] Database backup plan
  - [ ] Code repository backup (GitHub)
  - [ ] Regular backup schedule

## 💰 Cost Considerations

Understand the costs:

- [ ] **Vercel**
  - Free: 100GB bandwidth, serverless functions
  - Paid: Starts at $20/month for Pro
  
- [ ] **Railway**
  - Free: $5 credit/month
  - Paid: Usage-based, ~$5-20/month typically
  
- [ ] **Render**
  - Free: 750 hours/month, 90 days DB
  - Paid: Starts at $7/month for web service
  
- [ ] **Database (Neon/Supabase)**
  - Free tier sufficient for development
  - Paid plans start at $5-20/month
  
- [ ] **Groq API**
  - Free tier available
  - Monitor usage to avoid overages

## 📚 Documentation Review

- [ ] **Read Deployment Guide**
  - [ ] `DEPLOYMENT_GUIDE.md` reviewed
  - [ ] Chosen deployment strategy
  - [ ] Understand all steps required
  
- [ ] **Update Documentation**
  - [ ] Update README.md with deployment URLs (after deployment)
  - [ ] Document any custom configuration
  - [ ] Add production environment setup instructions

## ✅ Quick Validation Commands

Before deploying, run these locally:

```bash
# Backend validation
python -c "import fastapi, sqlalchemy, groq; print('All imports successful')"
uvicorn main:app --host 0.0.0.0 --port 8000 &
curl http://localhost:8000/docs
# Should show FastAPI docs

# Frontend validation
cd frontend
npm install
npm run build
# Should complete without errors

# Database validation
python init_db.py
# Should create tables successfully
```

## 🎯 Final Steps Before Deployment

1. [ ] One final commit with all changes
2. [ ] Push to GitHub
3. [ ] Double-check all API keys are in environment variables (not code)
4. [ ] Take a deep breath! 🧘
5. [ ] Follow the deployment guide step by step
6. [ ] Test the deployed application thoroughly

---

## ⚠️ Important Reminders

- **NEVER commit API keys or secrets to Git**
- **Always use environment variables for sensitive data**
- **Test locally before deploying**
- **Keep a backup of your database**
- **Monitor your application after deployment**
- **Start with free tiers to test before scaling**

---

## 🆘 Need Help?

If you encounter issues:

1. Check the deployment platform's logs
2. Review `DEPLOYMENT_GUIDE.md` for troubleshooting
3. Verify all environment variables are set correctly
4. Test backend and frontend separately
5. Check database connection
6. Review CORS settings

---

## ✨ Ready to Deploy!

Once all items are checked, proceed to `DEPLOYMENT_GUIDE.md` and choose your deployment option!

Good luck! 🚀
