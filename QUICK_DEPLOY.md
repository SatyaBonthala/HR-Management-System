# 🎯 Quick Deployment Reference

## Platform Comparison

| Feature | Vercel | Railway | Render |
|---------|--------|---------|--------|
| **Free Tier** | ✅ Yes | ✅ $5/month credit | ✅ True free |
| **Database Included** | ❌ No | ✅ Yes | ✅ Yes (90 days) |
| **Docker Support** | ❌ No | ✅ Yes | ✅ Yes |
| **Auto Deploy from Git** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Custom Domains** | ✅ Free | ✅ Free | ✅ Free |
| **Serverless** | ✅ Yes | ❌ No | ❌ No |
| **Best For** | Simple APIs | Docker projects | Full-stack apps |

---

## 🔗 Quick Links

### Get API Keys
- **Groq API** (Free): https://console.groq.com
- **OpenAI API** (Paid): https://platform.openai.com

### Database Services
- **Neon** (Free PostgreSQL): https://neon.tech ⭐ Recommended
- **Supabase** (Free PostgreSQL): https://supabase.com
- **Railway** (Included): https://railway.app
- **Render** (Free 90 days): https://render.com

### Deployment Platforms
- **Vercel**: https://vercel.com
- **Railway**: https://railway.app
- **Render**: https://render.com

---

## 📝 Quick Commands

### Check if ready to deploy
```bash
python check_deployment_ready.py
```

### Backend - Test locally
```bash
uvicorn main:app --reload
# Visit: http://localhost:8000/docs
```

### Frontend - Test locally
```bash
cd frontend
npm install
npm run dev
# Visit: http://localhost:5173
```

### Frontend - Build for production
```bash
cd frontend
npm run build
```

### Database - Initialize
```bash
python init_db.py
```

### Database - Seed test data
```bash
python seed_data.py
```

### Git - Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

---

## ⚡ Quick Start - Vercel (Recommended)

### 1. Database Setup (5 minutes)
1. Go to **neon.tech** → Sign up
2. Create new project → Copy connection string
3. Save it for step 3

### 2. GitHub Setup (2 minutes)
```bash
# If not already done:
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

### 3. Backend Deployment (10 minutes)
1. Go to **vercel.com** → Sign in
2. **New Project** → Import from GitHub
3. Select your repository
4. Add these environment variables:
   ```
   DATABASE_URL=your_neon_connection_string
   GROQ_API_KEY=your_groq_api_key
   SECRET_KEY=generate_random_string
   DEBUG=False
   ```
5. Click **Deploy**
6. Copy your backend URL: `https://your-project.vercel.app`

### 4. Initialize Database (3 minutes)
```bash
# Update DATABASE_URL in .env with your Neon connection string
python init_db.py
python seed_data.py  # Optional: Add test data
```

### 5. Frontend Deployment (5 minutes)
1. Update `frontend/.env.production`:
   ```
   VITE_API_URL=https://your-backend.vercel.app
   ```
2. Commit and push:
   ```bash
   git add .
   git commit -m "Add production config"
   git push
   ```
3. In Vercel → **New Project**
4. Import same repository
5. **Root Directory**: `frontend`
6. **Framework**: Vite
7. Add environment variable:
   ```
   VITE_API_URL=https://your-backend.vercel.app
   ```
8. Click **Deploy**

### 6. Update CORS (2 minutes)
1. Update `main.py` - add your frontend URL to CORS:
   ```python
   allow_origins=[
       "https://your-frontend.vercel.app",
   ]
   ```
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update CORS"
   git push
   ```

### 7. Test! 🎉
- Backend: `https://your-backend.vercel.app/docs`
- Frontend: `https://your-frontend.vercel.app`

---

## ⚡ Quick Start - Railway (Alternative)

### 1. Railway Setup
1. Go to **railway.app** → Sign up
2. **New Project** → Deploy from GitHub
3. Connect your repository

### 2. Add Database
1. Click **New** → **Database** → **PostgreSQL**
2. Database URL is auto-configured

### 3. Configure Environment Variables
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=generate_random_string
DEBUG=False
PORT=8000
```

### 4. Deploy
- Railway auto-deploys from Dockerfile
- Get your public URL from dashboard

### 5. Initialize Database
- Use Railway terminal or connect locally
- Run: `python init_db.py`

---

## 🐛 Quick Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Database connection fails
- Check DATABASE_URL format
- Ensure `?sslmode=require` for Neon/Supabase
- Test connection locally first

### CORS errors
- Update `main.py` CORS origins
- Add your frontend domain
- Redeploy backend

### Frontend can't connect to API
- Check VITE_API_URL in frontend
- Verify backend is running
- Check browser console for errors

### "Application failed to respond" (Vercel)
- Check function timeout (10s limit on free tier)
- Review logs in Vercel dashboard
- Consider Railway/Render for long operations

---

## 📊 Cost Estimates (Monthly)

### Free/Hobby Tier
- **Vercel** (Backend): Free (100GB bandwidth)
- **Vercel** (Frontend): Free (100GB bandwidth)
- **Neon** (Database): Free (3GB storage)
- **Groq API**: Free tier available
- **Total**: $0/month 🎉

### Starter Tier (Low Traffic)
- **Railway**: ~$5-10 (Pay for usage)
- **Neon**: Free tier
- **Groq API**: Free tier
- **Total**: ~$5-10/month

### Production Tier (Medium Traffic)
- **Vercel Pro**: $20/month
- **Neon Pro**: $19/month
- **Groq API**: Varies by usage
- **Total**: ~$40-60/month

---

## 📞 Support Resources

### Documentation
- See `DEPLOYMENT_GUIDE.md` for detailed instructions
- See `PRE_DEPLOYMENT_CHECKLIST.md` for complete checklist
- See `PROJECT_OVERVIEW.md` for system architecture

### Platform Docs
- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

### Community
- FastAPI Discord: https://discord.gg/VQjSZaeJmf
- Vercel Discord: https://vercel.com/discord
- Railway Discord: https://discord.gg/railway

---

## ✅ Success Checklist

After deployment:
- [ ] Backend API accessible at `/docs`
- [ ] Frontend loads correctly
- [ ] Can create positions
- [ ] Can add candidates
- [ ] Recruitment agent screens candidates
- [ ] Onboarding agent works
- [ ] No CORS errors
- [ ] Database persists data

---

**Ready to deploy? Run this first:**
```bash
python check_deployment_ready.py
```

**Then follow the detailed guide:**
```bash
# Read this file:
DEPLOYMENT_GUIDE.md
```

**Good luck! 🚀**
