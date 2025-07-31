# Deploy MentorIQ Backend - Choose Your Platform

## Option 1: Render (Recommended)
**Best for**: Python web services, free tier available

### Steps:
1. Go to https://dashboard.render.com/
2. New + → Web Service 
3. Connect GitHub → mentoriq-backend
4. Settings:
   ```
   Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
   Environment Variable: GROQ_API_KEY = [your_groq_api_key]
   ```
5. Create Web Service

**Result**: `https://mentoriq-backend.onrender.com`

---

## Option 2: Vercel (If you have Vercel account)
**Best for**: If you already use Vercel

### Steps:
```bash
# In backend directory
vercel login
vercel env add GROQ_API_KEY
# Enter your Groq API key when prompted
vercel --prod
```

**Result**: `https://mentoriq-backend.vercel.app`

---

## Option 3: Railway
**Best for**: Simple Python deployment

### Steps:
1. Go to https://railway.app/
2. New Project → Deploy from GitHub
3. Select mentoriq-backend
4. Add environment variable: `GROQ_API_KEY`
5. Deploy

---

## After Deployment

Once you get your backend URL (e.g., `https://mentoriq-backend.onrender.com`), let me know and I'll update the frontend to use it!

## Test Your Deployed Backend
```bash
curl https://your-backend-url.com/health
```

Should return: `{"status": "healthy", "groq_available": true}`