"""
Deployment Readiness Checker
This script checks if your project is ready for deployment
"""
import os
import sys
from pathlib import Path

def check_mark(condition):
    return "✅" if condition else "❌"

def check_env_file():
    """Check if .env file exists"""
    return os.path.exists('.env')

def check_env_example():
    """Check if .env.example exists"""
    return os.path.exists('.env.example')

def check_gitignore():
    """Check if .gitignore excludes .env"""
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            content = f.read()
            return '.env' in content
    return False

def check_requirements():
    """Check if requirements.txt exists"""
    return os.path.exists('requirements.txt')

def check_dockerfile():
    """Check if Dockerfile exists"""
    return os.path.exists('Dockerfile')

def check_vercel_config():
    """Check if vercel.json exists"""
    return os.path.exists('vercel.json')

def check_frontend_package():
    """Check if frontend/package.json exists"""
    return os.path.exists('frontend/package.json')

def check_git_initialized():
    """Check if git is initialized"""
    return os.path.exists('.git')

def check_env_variables():
    """Check critical environment variables"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'DATABASE_URL',
        'GROQ_API_KEY',
        'SECRET_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    return len(missing) == 0, missing

def main():
    print("=" * 60)
    print("🚀 DEPLOYMENT READINESS CHECK")
    print("=" * 60)
    print()
    
    # File checks
    print("📁 FILE CHECKS:")
    print(f"{check_mark(check_env_file())} .env file exists")
    print(f"{check_mark(check_env_example())} .env.example file exists")
    print(f"{check_mark(check_gitignore())} .gitignore excludes .env")
    print(f"{check_mark(check_requirements())} requirements.txt exists")
    print(f"{check_mark(check_dockerfile())} Dockerfile exists")
    print(f"{check_mark(check_vercel_config())} vercel.json exists")
    print(f"{check_mark(check_frontend_package())} frontend/package.json exists")
    print()
    
    # Git check
    print("🔧 GIT REPOSITORY:")
    git_init = check_git_initialized()
    print(f"{check_mark(git_init)} Git repository initialized")
    
    if git_init:
        # Check if there are uncommitted changes
        import subprocess
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, check=True)
            has_changes = bool(result.stdout.strip())
            print(f"{check_mark(not has_changes)} All changes committed")
            
            # Check if remote exists
            result = subprocess.run(['git', 'remote', '-v'], 
                                  capture_output=True, text=True, check=True)
            has_remote = bool(result.stdout.strip())
            print(f"{check_mark(has_remote)} Remote repository configured")
        except:
            print("⚠️  Could not check git status")
    print()
    
    # Environment variables check
    print("🔐 ENVIRONMENT VARIABLES:")
    try:
        env_ok, missing_vars = check_env_variables()
        print(f"{check_mark(env_ok)} All required variables set")
        if not env_ok:
            print(f"   Missing: {', '.join(missing_vars)}")
    except Exception as e:
        print(f"❌ Could not check environment variables")
        print(f"   Error: {str(e)}")
    print()
    
    # Dependencies check
    print("📦 DEPENDENCIES:")
    try:
        import fastapi
        print(f"✅ FastAPI installed ({fastapi.__version__})")
    except ImportError:
        print(f"❌ FastAPI not installed")
    
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy installed ({sqlalchemy.__version__})")
    except ImportError:
        print(f"❌ SQLAlchemy not installed")
    
    try:
        import groq
        print(f"✅ Groq installed")
    except ImportError:
        print(f"❌ Groq not installed")
    print()
    
    # Frontend check
    print("🎨 FRONTEND:")
    frontend_exists = os.path.exists('frontend')
    print(f"{check_mark(frontend_exists)} Frontend directory exists")
    
    if frontend_exists:
        node_modules = os.path.exists('frontend/node_modules')
        print(f"{check_mark(node_modules)} Node modules installed")
        
        dist_exists = os.path.exists('frontend/dist')
        print(f"{check_mark(dist_exists)} Build directory exists (run 'npm run build')")
    print()
    
    # Summary
    print("=" * 60)
    print("📋 NEXT STEPS:")
    print("=" * 60)
    print()
    print("1. Review PRE_DEPLOYMENT_CHECKLIST.md")
    print("2. Choose your deployment platform:")
    print("   • Vercel (Easiest, free tier)")
    print("   • Railway (Docker-based, $5/month free credit)")
    print("   • Render (True free tier)")
    print("3. Follow the step-by-step guide in DEPLOYMENT_GUIDE.md")
    print("4. Set up your database (Neon, Supabase, etc.)")
    print("5. Configure environment variables on your platform")
    print("6. Deploy and test!")
    print()
    print("=" * 60)
    print("Need help? Check DEPLOYMENT_GUIDE.md for detailed instructions")
    print("=" * 60)

if __name__ == "__main__":
    main()
