# 🧪 Testing Guide - Interview Simulator

## ✅ Pre-Flight Checklist

Before starting, ensure:
- [ ] Docker Desktop is running
- [ ] Ports 8000, 5433, 3000 are available
- [ ] You have ~4GB free RAM
- [ ] Microphone is connected and working

---

## 🚀 Step-by-Step Testing

### **1. Backend Health Check**

**Start Backend:**
```powershell
cd c:\Users\user\Desktop\AUTOATED-CANDIDATE-SCREENING-AGENT_HireMind_5DS2-youssef\ai_hiring_app
docker-compose up --build
```

**Wait for these logs:**
```
api_1  | INFO:     ✓ Wav2Vec2 model loaded successfully
api_1  | INFO:     ✓ Stress recognition model loaded successfully
api_1  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test in Browser:**
1. Open: http://localhost:8000
   - Should see: `{"message": "Welcome to the AI Hiring API"}`

2. Open: http://localhost:8000/interview/health
   - Should see:
   ```json
   {
     "status": "healthy",
     "module": "interview_simulator",
     "voice_analyzer": "ready",
     "models": {
       "wav2vec2": "loaded",
       "stress_recognition": "loaded"
     }
   }
   ```

3. Open: http://localhost:8000/docs
   - Should see interactive API documentation
   - Look for `/interview/analyze-voice` endpoint

✅ **Backend is ready!**

---

### **2. Frontend Setup**

**Open New Terminal:**
```powershell
cd c:\Users\user\Desktop\AUTOATED-CANDIDATE-SCREENING-AGENT_HireMind_5DS2-youssef\frontend
npm install
npm start
```

**Wait for:**
```
Compiled successfully!
You can now view hiremind-interview-frontend in the browser.
  Local:            http://localhost:3000
```

**Browser should auto-open to:** http://localhost:3000

**You should see:**
- Purple gradient background
- Header: "🎤 HireMind Interview Simulator"
- White card with recording interface
- "Start Recording" button

✅ **Frontend is ready!**

---

### **3. End-to-End Voice Analysis Test**

#### **Test 1: Basic Recording**

1. **Click "Start Recording"**
   - Should see:
     - Red pulsing dot
     - "Recording... 00:00" timer
     - "Stop Recording" button (red)

2. **Speak for 5 seconds**
   - Say something calm like: "Hello, my name is [your name]. I am excited about this opportunity."

3. **Click "Stop Recording"**
   - Should see:
     - Audio player with your recording
     - "Analyze Voice" button (green)
     - "New Recording" button (gray)

4. **Play back your recording**
   - Verify audio quality is good

5. **Click "Analyze Voice"**
   - Should see:
     - "Analyzing..." with spinner (2-5 seconds)
     - Then results appear!

**Expected Results:**
- **Stress Classification:** Likely "Not Stressed" or "Low"
- **Probability bars:** Higher green bar
- **Feedback:** Positive message
- **Metadata:** Duration should match recording time

✅ **Basic test passed!**

---

#### **Test 2: Stressed Voice Simulation**

1. **Click "New Recording"**
2. **Click "Start Recording"**
3. **Simulate stress:**
   - Speak quickly
   - Take short breaths
   - Use higher pitch
   - Add hesitation: "Um... uh... I think... maybe..."
   - Example: "Um, so, like, I was, uh, working on this project and, um, things got really, uh, complicated..."

4. **Stop and Analyze**

**Expected Results:**
- **Stress Classification:** "Moderate" or "High"
- **Probability bars:** Higher red bar
- **Feedback:** Suggestions for improvement
- **Stress emoji:** 😐 or 😰

✅ **Stress detection working!**

---

#### **Test 3: Different Recording Lengths**

**Short (3 seconds):**
- Should work but may be less accurate

**Medium (10 seconds):**
- Optimal length for analysis

**Long (30+ seconds):**
- Should work, may take slightly longer to process

✅ **Various durations handled!**

---

### **4. Error Handling Tests**

#### **Test 4: No Audio**
1. Click "Start Recording"
2. Immediately click "Stop Recording" (no speech)
3. Try to analyze

**Expected:** Should still process (silence is valid audio)

---

#### **Test 5: Multiple Recordings**
1. Record → Analyze → View Results
2. Click "New Recording"
3. Record again → Analyze

**Expected:** Each analysis should be independent and accurate

---

#### **Test 6: Browser Permissions**
1. Deny microphone access
2. Click "Start Recording"

**Expected:** Error message about microphone permissions

---

### **5. API Direct Testing (Optional)**

If you want to test the backend directly without frontend:

**Using PowerShell:**
```powershell
# Create a test audio file first, then:
$filePath = "C:\path\to\test-audio.wav"
curl.exe -X POST "http://localhost:8000/interview/analyze-voice" `
  -F "file=@$filePath"
```

**Using API Docs (Easier):**
1. Go to: http://localhost:8000/docs
2. Find `POST /interview/analyze-voice`
3. Click "Try it out"
4. Upload an audio file
5. Click "Execute"
6. View JSON response

---

## 📊 Performance Benchmarks

### **Expected Timings**

| Operation | Expected Time |
|-----------|---------------|
| Backend startup (first time) | 5-10 minutes |
| Backend startup (cached) | 30-60 seconds |
| Frontend startup | 10-20 seconds |
| Model loading (first request) | 10-30 seconds |
| Audio analysis (5s audio) | 1-2 seconds |
| Audio analysis (15s audio) | 2-3 seconds |

### **Memory Usage**

| Component | Expected RAM |
|-----------|--------------|
| Docker (Backend) | 2-3 GB |
| React (Frontend) | 100-200 MB |
| PostgreSQL | 50-100 MB |
| **Total** | **~3-4 GB** |

---

## 🐛 Common Issues & Solutions

### **Issue 1: "Models not loaded"**

**Symptoms:** 
- `/interview/health` shows error
- Analysis fails with 503 error

**Solutions:**
1. Wait longer (first load takes time)
2. Check Docker logs: `docker-compose logs api`
3. Restart containers: `docker-compose restart`
4. Increase Docker memory limit (Settings → Resources)

---

### **Issue 2: "Microphone not working"**

**Symptoms:**
- "Start Recording" does nothing
- Permission error

**Solutions:**
1. Allow microphone in browser (check address bar)
2. Check Windows microphone settings
3. Try different browser (Chrome recommended)
4. Ensure using HTTPS or localhost (MediaRecorder requirement)

---

### **Issue 3: "CORS error"**

**Symptoms:**
- Frontend can't reach backend
- Network error in console

**Solutions:**
1. Ensure backend is running on port 8000
2. Check `main.py` has CORS middleware (already added)
3. Verify frontend is on port 3000
4. Try hard refresh: Ctrl+Shift+R

---

### **Issue 4: "Analysis takes too long"**

**Symptoms:**
- Spinner runs for >30 seconds

**Solutions:**
1. Check backend logs for errors
2. Try shorter audio clip
3. Restart backend container
4. Check CPU usage (may be overloaded)

---

### **Issue 5: "Low confidence scores"**

**Symptoms:**
- Confidence always <50%

**Solutions:**
1. Speak louder and clearer
2. Reduce background noise
3. Use better microphone
4. Ensure at least 5 seconds of speech
5. This is expected for ambiguous/neutral speech

---

## 🎯 Test Scenarios

### **Scenario 1: Confident Answer**
**Script:** "I have over 5 years of experience in software development. I specialize in Python and machine learning. I'm confident in my ability to contribute to your team."

**Expected:** Low stress, high confidence

---

### **Scenario 2: Nervous Answer**
**Script:** "Um... well... I think I have some experience, uh, maybe 2 or 3 years? I'm, uh, not really sure if I'm the best fit, but I'll try my best..."

**Expected:** High stress, clear detection

---

### **Scenario 3: Excited Answer**
**Script:** "I'm so excited about this role! I've been following your company for years and I really believe in your mission!"

**Expected:** Low-Moderate stress (excitement can register as slight stress)

---

### **Scenario 4: Technical Answer**
**Script:** "In my last project, I implemented a microservices architecture using Docker and Kubernetes. We reduced deployment time by 60% and improved system reliability."

**Expected:** Low stress (matter-of-fact delivery)

---

## ✅ Validation Checklist

After testing, verify:

**Backend:**
- [x] API responds on port 8000
- [x] Health check returns "healthy"
- [x] Models load successfully
- [x] Audio upload accepted
- [x] Analysis returns valid JSON
- [x] Error handling works

**Frontend:**
- [x] UI renders correctly
- [x] Recording starts/stops
- [x] Audio playback works
- [x] Analysis button functional
- [x] Results display properly
- [x] Animations smooth
- [x] Responsive on mobile

**Integration:**
- [x] Frontend → Backend communication
- [x] File upload successful
- [x] Results received and displayed
- [x] Error messages shown
- [x] CORS working

---

## 📈 Success Metrics

**You'll know it's working when:**
1. ✅ You can record and play back audio
2. ✅ Analysis completes in <5 seconds
3. ✅ Results show different stress levels for different tones
4. ✅ Confident speech → Low stress
5. ✅ Nervous speech → High stress
6. ✅ UI is responsive and smooth
7. ✅ No console errors

---

## 🎓 Advanced Testing

### **Test with Real Interview Questions**

1. Find a list of common interview questions
2. Record yourself answering each
3. Compare stress levels
4. Practice until you see improvement!

### **A/B Testing**

1. Answer the same question twice
2. First time: unprepared
3. Second time: well-practiced
4. Compare stress scores

**Expected:** Prepared answer should have lower stress!

---

## 📞 Support

If issues persist:
1. Check all logs: `docker-compose logs`
2. Verify all dependencies installed
3. Try clean rebuild: `docker-compose down -v && docker-compose up --build`
4. Check system resources (RAM, disk space)

---

**Happy Testing!** 🎉

Remember: The goal is to help candidates improve their interview skills through AI-powered feedback!
