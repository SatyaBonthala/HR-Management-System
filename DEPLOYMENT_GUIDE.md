# 🚀 Deployment Guide - HR Management System

This guide covers three deployment strategies for your AI-powered HR Management System.

---

## 🎯 Option 1: Vercel Deployment (Recommended for Beginners)

### **Advantages:**
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy GitHub integration
- ✅ Fast deployment
- ✅ Great for serverless

### **Pre-requisites:**
1. GitHub account
2. Vercel account (free at vercel.com)
3. Neon or Supabase account (free PostgreSQL)
4. Groq API key (from console.groq.com)

### **Step 1: Prepare Your Repository**

1. **Initialize Git (if not already done):**
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Create a new repository on GitHub:**
   - Go to github.com
   - Click "New repository"
   - Name it "hr-management-system"
   - Don't initialize with README (you already have one)

3. **Push your code:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/hr-management-system.git
git branch -M main
git push -u origin main
```

### **Step 2: Set Up PostgreSQL Database**

#### Using Neon (Recommended):

1. Go to **neon.tech**
2. Sign up for a free account
3. Click **"Create Project"**
4. Name it "hr-management"
5. Select region closest to you
6. Copy the **connection string** (looks like: `postgresql://user:pass@host.neon.tech/dbname?sslmode=require`)

#### Alternative - Supabase:

1. Go to **supabase.com**
2. Create new project
3. Go to Settings → Database
4. Copy **Connection String** (URI format)

### **Step 3: Deploy Backend API to Vercel**

1. **Go to vercel.com and sign in**

2. **Click "Add New" → "Project"**

3. **Import your GitHub repository**

4. **Configure the project:**
   - **Framework Preset:** Other
   - **Root Directory:** `./` (leave as is)
   - **Build Command:** Leave empty
   - **Output Directory:** Leave empty

5. **Add Environment Variables:**
   Click "Environment Variables" and add:

   ```
   DATABASE_URL = your_neon_or_supabase_connection_string
   GROQ_API_KEY = your_groq_api_key
   APP_NAME = Agentic HR Management System
   DEBUG = False
   SECRET_KEY = generate_a_random_string_here
   RECRUITMENT_AGENT_MODEL = llama-3.3-70b-versatile
   ONBOARDING_AGENT_MODEL = llama-3.3-70b-versatile
   AGENT_TEMPERATURE = 0.7
   AGENT_MAX_TOKENS = 2000
   ```

   **To generate SECRET_KEY:**
   ```python
   # Run in Python:
   import secrets
   print(secrets.token_urlsafe(32))
   ```

6. **Click "Deploy"**

7. **Initialize Database:**
   After deployment, you need to initialize your database tables.
   
   - Go to your project in Vercel
   - Click on "Deployments"
   - Click on your latest deployment
   - Go to "Functions" tab
   - Note your deployment URL (e.g., `https://your-project.vercel.app`)
   
   Then run locally:
   ```bash
   # Update DATABASE_URL in your local .env file with Neon/Supabase URL
   python init_db.py
   ```

8. **Your API is now live!** 
   - API URL: `https://your-project.vercel.app`
   - Test it: `https://your-project.vercel.app/docs` (FastAPI docs)

### **Step 4: Deploy Frontend to Vercel**

1. **Update Frontend API Configuration:**
   
   You need to create a production config file for the frontend.

   Create `frontend/.env.production`:
   ```
   VITE_API_URL=https://your-backend-project.vercel.app
   ```

2. **Create a new Vercel project for frontend:**
   - Click "Add New" → "Project"
   - Select your same GitHub repository
   - Click "Add"

3. **Configure frontend project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

4. **Add Environment Variable:**
   ```
   VITE_API_URL = https://your-backend-project.vercel.app
   ```

5. **Click "Deploy"**

6. **Your frontend is now live!**
   - Frontend URL: `https://your-frontend.vercel.app`

### **Step 5: Update CORS Settings**

Update your `main.py` to allow your frontend domain:

```python
# In main.py, update CORS origins:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-frontend.vercel.app",  # Add your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push:
```bash
git add .
git commit -m "Update CORS settings"
git push
```

Vercel will automatically redeploy your backend!

---

## 🚂 Option 2: Railway Deployment (Docker-based)

### **Advantages:**
- ✅ Built-in PostgreSQL
- ✅ Supports Docker
- ✅ Simple dashboard
- ✅ $5/month free credit

### **Steps:**

1. **Go to railway.app and sign up**

2. **Create a new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your repository

3. **Add PostgreSQL:**
   - Click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will create a database

4. **Configure your application:**
   - Railway automatically detects your Dockerfile
   - Click on your service
   - Go to "Variables" tab

5. **Add Environment Variables:**
   ```
   DATABASE_URL = ${{Postgres.DATABASE_URL}}  # Railway provides this
   GROQ_API_KEY = your_groq_api_key
   APP_NAME = Agentic HR Management System
   DEBUG = False
   SECRET_KEY = generate_random_string
   RECRUITMENT_AGENT_MODEL = llama-3.3-70b-versatile
   ONBOARDING_AGENT_MODEL = llama-3.3-70b-versatile
   AGENT_TEMPERATURE = 0.7
   AGENT_MAX_TOKENS = 2000
   PORT = 8000
   ```

6. **Deploy:**
   - Railway automatically deploys
   - Get your public URL from the dashboard

7. **Initialize Database:**
   - Use Railway's terminal or connect with your local tool
   - Run: `python init_db.py`

8. **Deploy Frontend:**
   For frontend, you can:
   - Deploy to Vercel (follow Option 1, Step 4)
   - OR create another Railway service from the `frontend` directory

---

## 🎨 Option 3: Render (Free Tier Available)

### **Advantages:**
- ✅ True free tier (no credit card required)
- ✅ Auto-deploy from GitHub
- ✅ Managed PostgreSQL (free 90 days)

### **Steps:**

#### **A. Deploy Database:**

1. **Go to render.com and sign up**

2. **Create PostgreSQL database:**
   - Click "New" → "PostgreSQL"
   - Name: `hr-management-db`
   - Select free tier
   - Click "Create Database"
   - Copy the **Internal Database URL**

#### **B. Deploy Backend:**

1. **Create Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** `hr-management-api`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Plan:** Free

2. **Add Environment Variables:**
   ```
   DATABASE_URL = your_internal_database_url_from_step_A2
   GROQ_API_KEY = your_groq_api_key
   APP_NAME = Agentic HR Management System
   DEBUG = False
   SECRET_KEY = generate_random_string
   RECRUITMENT_AGENT_MODEL = llama-3.3-70b-versatile
   ONBOARDING_AGENT_MODEL = llama-3.3-70b-versatile
   AGENT_TEMPERATURE = 0.7
   AGENT_MAX_TOKENS = 2000
   PYTHON_VERSION = 3.11.0
   ```

3. **Click "Create Web Service"**

4. **Initialize Database:**
   - Once deployed, go to "Shell" tab
   - Run: `python init_db.py`

5. **Your API URL:** `https://hr-management-api.onrender.com`

#### **C. Deploy Frontend:**

1. **Create Static Site:**
   - Click "New" → "Static Site"
   - Connect your repository
   - Configure:
     - **Name:** `hr-management-frontend`
     - **Root Directory:** `frontend`
     - **Build Command:** `npm install && npm run build`
     - **Publish Directory:** `frontend/dist`

2. **Add Environment Variable:**
   ```
   VITE_API_URL = https://hr-management-api.onrender.com
   ```

3. **Click "Create Static Site"**

4. **Your frontend URL:** `https://hr-management-frontend.onrender.com`

5. **Update CORS in backend** (see Option 1, Step 5)

---

## 🐳 Option 4: Docker on VPS (DigitalOcean, AWS, etc.)

### **For Advanced Users:**

If you want full control, you can deploy on a VPS:

1. **Set up a VPS** (DigitalOcean Droplet, AWS EC2, etc.)

2. **Install Docker and Docker Compose:**
```bash
# On Ubuntu:
sudo apt update
sudo apt install docker.io docker-compose -y
```

3. **Clone your repository on the server:**
```bash
git clone https://github.com/YOUR_USERNAME/hr-management-system.git
cd hr-management-system
```

4. **Create `.env` file:**
```bash
OPENAI_API_KEY=your_key_here
```

5. **Start services:**
```bash
docker-compose up -d
```

6. **Initialize database:**
```bash
docker exec -it hr_system_api python init_db.py
```

7. **Set up Nginx reverse proxy** (for HTTPS and domain)

8. **Deploy frontend:**
```bash
cd frontend
npm install
npm run build
# Copy dist/ folder to web server
```

---

## 📝 Post-Deployment Checklist

After deploying, verify:

- [ ] Backend API is accessible
- [ ] `/docs` endpoint shows FastAPI documentation
- [ ] Database tables are created (run init_db.py)
- [ ] Frontend loads correctly
- [ ] Frontend can connect to backend API
- [ ] Create test candidate and application
- [ ] Test AI agents (recruitment and onboarding)
- [ ] Check logs for any errors

---

## 🔧 Common Issues & Solutions

### Issue: "Module not found" error
**Solution:** Make sure all dependencies are in `requirements.txt`

### Issue: Database connection fails
**Solution:** 
- Check DATABASE_URL is correct
- Ensure database allows external connections
- For Neon/Supabase, ensure `?sslmode=require` is in URL

### Issue: CORS errors in frontend
**Solution:** Update CORS origins in `main.py` to include your frontend domain

### Issue: "Application failed to respond" on Vercel
**Solution:** 
- Vercel has limits on serverless functions (10 seconds timeout on free tier)
- Consider using Railway or Render for long-running operations

### Issue: Frontend can't connect to API
**Solution:** 
- Check VITE_API_URL in frontend environment variables
- Ensure backend CORS allows frontend domain
- Check browser console for specific errors

---

## 🎉 Success!

Once deployed, your HR Management System will be live and accessible from anywhere!

**Next Steps:**
1. Seed initial data (`python seed_data.py`)
2. Create test candidates and positions
3. Test the recruitment agent
4. Test the onboarding agent
5. Monitor logs for any issues
6. Set up custom domain (optional)

---

## 💡 Tips

- **Use environment-specific configs** for development vs production
- **Enable monitoring** (Vercel Analytics, Render metrics, etc.)
- **Set up alerts** for errors
- **Keep your API keys secure** - never commit them to Git
- **Regular backups** of your database
- **Monitor API usage** for Groq API costs

---

## 📚 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Neon Documentation](https://neon.tech/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)

---

Need help? Check the logs:
- **Vercel:** Project → Deployments → Click deployment → Logs
- **Railway:** Project → Service → Deployments → View logs
- **Render:** Dashboard → Service → Logs tab
