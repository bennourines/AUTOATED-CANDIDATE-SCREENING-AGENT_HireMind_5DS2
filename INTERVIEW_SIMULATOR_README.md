# 🎤 HireMind Interview Simulator - Phase 1: Voice Stress Analysis

## 📋 Overview

This is **Phase 1** of the HireMind Interview Simulator, focusing on **AI-powered voice stress detection** during interview responses. The system uses advanced machine learning models to analyze a candidate's voice and provide insights about their stress levels.

---

## 🏗️ Architecture

### **Backend (FastAPI + PyTorch)**
```
ai_hiring_app/
├── app/
│   ├── main.py                          # Main FastAPI application
│   ├── models.py                        # Database models
│   ├── schemas.py                       # Pydantic schemas (includes VoiceAnalysisResult)
│   ├── database.py                      # Database configuration
│   ├── ai_modules/                      # Resume parsing & matching (existing)
│   │   ├── resume_parser.py
│   │   └── matching_engine.py
│   └── interview_simulator/             # NEW: Interview module
│       ├── __init__.py
│       └── voice_analyzer.py            # Voice stress analysis engine
├── requirements.txt                     # Python dependencies (updated)
├── Dockerfile                           # Docker configuration (updated)
└── docker-compose.yml                   # Multi-container setup
```

### **Frontend (React)**
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── index.js
│   ├── index.css
│   ├── App.js
│   ├── App.css
│   └── components/
│       ├── VoiceRecorder.js             # Audio recording interface
│       ├── VoiceRecorder.css
│       ├── StressResults.js             # Results visualization
│       └── StressResults.css
└── package.json
```

---

## 🧠 AI Technology Stack

### **1. Wav2Vec2 (Facebook AI)**
- **Purpose**: Audio feature extraction
- **Model**: `torchaudio.pipelines.WAV2VEC2_BASE`
- **Function**: Converts raw audio → 512-dimensional embeddings
- **Why**: State-of-the-art self-supervised learning for speech

### **2. StudentNet Stress Recognition**
- **Model**: `forwarder1121/voice-based-stress-recognition`
- **Source**: HuggingFace Transformers
- **Architecture**: Lightweight MLP (Multi-Layer Perceptron)
- **Training**: Knowledge distillation from multimodal TeacherNet
- **Accuracy**: ~76% on StressID dataset
- **Output**: Binary classification (stressed/not stressed) with probabilities

### **3. Processing Pipeline**
```
Raw Audio (WebM/WAV/MP3)
    ↓
Preprocessing (Resampling, Mono Conversion)
    ↓
Wav2Vec2 Feature Extraction (512-dim embedding)
    ↓
StudentNet Classification
    ↓
Stress Probabilities + Level (Low/Moderate/High/Very High)
```

---

## 🚀 How to Run

### **Prerequisites**
- Docker Desktop installed and running
- Node.js (v16+) and npm installed

---

### **Step 1: Start Backend (Docker)**

```powershell
# Navigate to backend directory
cd c:\Users\user\Desktop\AUTOATED-CANDIDATE-SCREENING-AGENT_HireMind_5DS2-youssef\ai_hiring_app

# Build and start containers
docker-compose up --build
```

**What happens:**
- PostgreSQL database starts on port 5433
- FastAPI backend starts on port 8000
- Downloads ML models (Wav2Vec2 + Stress Recognition)
- Installs PyTorch, TorchAudio, Transformers

**Wait for:**
```
api_1  | INFO:     Uvicorn running on http://0.0.0.0:8000
api_1  | INFO:     ✓ Wav2Vec2 model loaded successfully
api_1  | INFO:     ✓ Stress recognition model loaded successfully
```

**Verify Backend:**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/interview/health

---

### **Step 2: Start Frontend (React)**

Open a **new PowerShell window**:

```powershell
# Navigate to frontend directory
cd c:\Users\user\Desktop\AUTOATED-CANDIDATE-SCREENING-AGENT_HireMind_5DS2-youssef\frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

**Frontend will open at:** http://localhost:3000

---

## 🎯 How to Use

### **1. Recording Your Voice**
1. Click **"Start Recording"** button
2. Speak your interview answer (minimum 5-10 seconds recommended)
3. Click **"Stop Recording"** when finished

### **2. Playback**
- Use the audio player to review your recording
- Ensure audio quality is good before analysis

### **3. Analyze**
- Click **"Analyze Voice"** button
- Wait 2-5 seconds for AI processing

### **4. View Results**
You'll receive:
- **Stress Classification**: Stressed vs Not Stressed
- **Stress Level**: Low, Moderate, High, or Very High
- **Confidence Score**: Model's certainty (0-100%)
- **Probability Breakdown**: Visual bars showing stress vs calm
- **Personalized Feedback**: Tips based on your stress level
- **Audio Metadata**: Duration and sample rate

---

## 📡 API Endpoints

### **Interview Module**

#### `POST /interview/analyze-voice`
Upload audio file and get stress analysis.

**Request:**
```bash
curl -X POST "http://localhost:8000/interview/analyze-voice" \
  -F "file=@recording.wav"
```

**Response:**
```json
{
  "not_stressed_probability": 0.25,
  "stressed_probability": 0.75,
  "is_stressed": true,
  "confidence": 0.75,
  "stress_level": "High",
  "sample_rate": 16000,
  "duration_seconds": 5.3
}
```

**Supported Formats:**
- `.wav` (recommended)
- `.mp3`
- `.m4a`
- `.flac`
- `.ogg`
- `.webm`

---

#### `GET /interview/health`
Check if interview module is ready.

**Response:**
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

---

## 🔧 Technical Details

### **Audio Processing**

**1. Preprocessing (`voice_analyzer.py`)**
```python
- Loads audio from bytes (any format via torchaudio)
- Converts stereo → mono (if needed)
- Resamples to 16kHz (Wav2Vec2 requirement)
```

**2. Feature Extraction**
```python
- Wav2Vec2 extracts contextual features
- Mean pooling over time dimension
- Output: (1, 512) embedding tensor
```

**3. Stress Prediction**
```python
- StudentNet MLP processes embedding
- Softmax produces probabilities
- Threshold-based classification
```

### **Stress Level Mapping**
| Stress Probability | Level      | Color  | Emoji |
|--------------------|------------|--------|-------|
| 0.0 - 0.3          | Low        | Green  | 😊    |
| 0.3 - 0.6          | Moderate   | Orange | 😐    |
| 0.6 - 0.8          | High       | Red    | 😰    |
| 0.8 - 1.0          | Very High  | Dark Red | 😫  |

---

## 🎨 Frontend Features

### **VoiceRecorder Component**
- Real-time recording with MediaRecorder API
- Recording timer (MM:SS format)
- Visual recording indicator (pulsing red dot)
- Audio playback before analysis
- Error handling with user-friendly messages

### **StressResults Component**
- Animated result appearance
- Color-coded stress indicators
- Probability visualization (progress bars)
- Personalized feedback based on stress level
- Actionable tips for improvement
- Responsive design (mobile-friendly)

---

## 🧪 Testing

### **Test with Sample Questions**

**Easy Question (Low Stress):**
> "Tell me about yourself."

**Moderate Question:**
> "What are your greatest strengths and weaknesses?"

**High-Pressure Question (High Stress):**
> "Describe a time when you failed and how you recovered."

### **Expected Behavior**
- Calm, prepared answers → Low stress
- Nervous, hesitant speech → Moderate-High stress
- Fast speech, vocal tension → High-Very High stress

---

## 📦 Dependencies

### **Backend (Python)**
```
Core:
- fastapi
- uvicorn
- pydantic
- sqlalchemy

ML & Audio:
- torch>=2.0.0
- torchaudio>=2.0.0
- transformers>=4.30.0
- librosa>=0.10.0
- soundfile>=0.12.0

NLP:
- spacy
```

### **Frontend (React)**
```
- react ^18.2.0
- react-dom ^18.2.0
- axios ^1.6.0
- recharts ^2.10.0
```

---

## 🔮 Future Enhancements (Phase 2 & 3)

### **Phase 2: Advanced Audio Analysis**
- [ ] Pause detection (silence segments)
- [ ] Filler word counting ("um", "uh", "like")
- [ ] Speech rate analysis (words per minute)
- [ ] Pitch variation tracking
- [ ] Volume consistency measurement

### **Phase 3: Question Bank Integration**
- [ ] Database of interview questions by job field
- [ ] Dynamic question suggestion based on role
- [ ] Progressive difficulty levels
- [ ] Question-answer session management
- [ ] Comprehensive interview reports

### **Phase 4: Advanced Features**
- [ ] Speech-to-text transcription (Whisper)
- [ ] Answer quality assessment (content analysis)
- [ ] Eye contact detection (computer vision)
- [ ] Body language analysis
- [ ] Comparative analytics (track improvement)
- [ ] Interview coaching recommendations

---

## 🐛 Troubleshooting

### **Backend Issues**

**Problem:** Models not loading
```
Solution: Ensure Docker has enough memory (4GB+ recommended)
Check: docker stats
```

**Problem:** Audio file error
```
Solution: 
- Ensure file is valid audio format
- Check file size (recommend <10MB)
- Try converting to WAV format
```

### **Frontend Issues**

**Problem:** Microphone access denied
```
Solution:
- Grant browser permission for microphone
- Use HTTPS or localhost (required for MediaRecorder)
- Check system microphone settings
```

**Problem:** CORS error
```
Solution:
- Ensure backend is running on port 8000
- Check CORS settings in main.py (already configured)
```

---

## 📊 Performance

### **Model Loading Time**
- First request: 10-30 seconds (models download & load)
- Subsequent requests: <1 second (models cached)

### **Analysis Speed**
- 5-second audio: ~1-2 seconds processing
- 10-second audio: ~2-3 seconds processing

### **Memory Usage**
- Backend: ~2-3 GB (PyTorch models)
- Frontend: ~100 MB

---

## 📝 Code Quality

### **Backend Best Practices**
- ✅ Singleton pattern for model loading (efficient)
- ✅ Comprehensive error handling
- ✅ Logging for debugging
- ✅ Type hints throughout
- ✅ Pydantic validation
- ✅ Async file upload handling

### **Frontend Best Practices**
- ✅ React hooks (useState, useRef)
- ✅ Component composition
- ✅ CSS animations
- ✅ Responsive design
- ✅ Error boundary handling
- ✅ Clean code structure

---

## 🤝 Contributing

To add new features:
1. Backend: Add to `app/interview_simulator/`
2. Update schemas in `app/schemas.py`
3. Add endpoints in `app/main.py`
4. Frontend: Create components in `frontend/src/components/`

---

## 📄 License

This project is part of the HireMind automated candidate screening system.

---

## 👨‍💻 Author

Developed as part of the HireMind project by **Youssef**

**Phase 1 Complete!** 🎉

Ready for Phase 2 development when you are! 🚀
