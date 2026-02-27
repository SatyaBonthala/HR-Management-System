"""
Vercel serverless function entry point
"""
from main import app

# Export the app for Vercel
handler = app
