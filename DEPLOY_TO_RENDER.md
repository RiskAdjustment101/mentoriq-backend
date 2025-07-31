# Deploy MentorIQ Backend to Render

## Quick Deploy Steps

### 1. Push Backend to GitHub
First, create a new GitHub repository for the backend:

```bash
# In the backend directory
cd backend
git remote add origin https://github.com/YOUR_USERNAME/mentoriq-backend.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your `mentoriq-backend` repository
5. Render will auto-detect settings from `render.yaml`

### 3. Configure Environment Variables

In Render Dashboard → Environment:

```
GROQ_API_KEY = your_groq_api_key_here
ALLOWED_ORIGINS = https://mentoriq.netlify.app,http://localhost:5173
```

### 4. Deploy!

Click **"Create Web Service"**

Your backend URL will be: `https://mentoriq-backend.onrender.com`

### 5. Update Frontend

In your main project, update `.env.production`:

```env
VITE_API_URL=https://mentoriq-backend.onrender.com
```

Then push to trigger Netlify redeploy.

## Free Tier Notes

- Render free tier spins down after 15 mins of inactivity
- First request after spin-down takes ~30 seconds
- Consider upgrading for always-on service ($7/month)

## Verify Deployment

Test your API:
```bash
curl https://mentoriq-backend.onrender.com/health
```

## Troubleshooting

- Check Render logs in dashboard
- Ensure Python version matches (3.11.7)
- Verify environment variables are set
- Check CORS origins include your Netlify URL