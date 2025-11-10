# 🚀 Quick Start Guide - Interview Simulator

## ⚡ 3-Step Setup

### Step 1: Start Backend (Terminal 1)
```powershell
cd c:\Users\user\Desktop\AUTOATED-CANDIDATE-SCREENING-AGENT_HireMind_5DS2-youssef\ai_hiring_app
docker-compose up --build
```
**Wait for:** `Uvicorn running on http://0.0.0.0:8000`

---

### Step 2: Start Frontend (Terminal 2 - New Window)
```powershell
cd c:\Users\user\Desktop\AUTOATED-CANDIDATE-SCREENING-AGENT_HireMind_5DS2-youssef\frontend
npm install
npm start
```
**Opens:** http://localhost:3000

---

### Step 3: Test It!
1. Click **"Start Recording"**
2. Speak for 5-10 seconds
3. Click **"Stop Recording"**
4. Click **"Analyze Voice"**
5. View your stress analysis! 📊

---

## 🔗 Important URLs

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/interview/health |

---

## ⚠️ First-Time Setup Notes

**Backend (Docker):**
- First build takes 5-10 minutes (downloads ML models)
- Requires ~4GB RAM
- Models are cached after first run

**Frontend (React):**
- `npm install` takes 2-3 minutes first time
- Only needed once

---

## 🎤 Usage Tips

**For Best Results:**
- Speak clearly for at least 5-10 seconds
- Use a quiet environment
- Grant microphone permissions
- Test with different stress levels

**Sample Questions to Try:**
1. "Tell me about yourself" (should be calm)
2. "Describe your biggest failure" (may show stress)
3. Practice the same answer multiple times to see improvement!

---

## 🐛 Quick Fixes

**Backend not starting?**
- Check Docker Desktop is running
- Ensure ports 8000 & 5433 are free

**Microphone not working?**
- Allow browser microphone access
- Check system microphone settings

**Analysis failing?**
- Wait for models to fully load (check logs)
- Try shorter recordings first (5-10 seconds)

---

## 📚 Full Documentation

See `INTERVIEW_SIMULATOR_README.md` for complete documentation.

---

**Ready to revolutionize interviews with AI!** 🎯
