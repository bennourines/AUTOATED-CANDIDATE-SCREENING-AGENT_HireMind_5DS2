"""
Streamlit Demo for HireMind Interview System.

Features:
- Interview question generation
- Answer recording (audio + video)
- Real-time cheating detection
- Avatar generation from CV
- Comprehensive evaluation
"""

import streamlit as st
import asyncio
import sys
import os
from pathlib import Path
import json
import tempfile
from datetime import datetime


# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from crews.interview_orchestrator import orchestrator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# helper function

def log_error(error_msg: str, exception: Exception = None):
    """Log error with details and display to user."""
    logger.error(error_msg)
    if exception:
        logger.error(f"Exception details: {str(exception)}")
        import traceback
        logger.error(traceback.format_exc())
    
    st.error(f"❌ {error_msg}")
    
    if exception:
        with st.expander("🔍 Technical Details"):
            st.code(str(exception))
            if st.checkbox("Show Full Traceback"):
                import traceback
                st.code(traceback.format_exc())


# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="HireMind - AI Interview System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .danger-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════

if 'questions' not in st.session_state:
    st.session_state.questions = []

if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0

if 'results' not in st.session_state:
    st.session_state.results = []

if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False

if 'interview_completed' not in st.session_state:
    st.session_state.interview_completed = False

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def reset_interview():
    """Reset interview state."""
    st.session_state.questions = []
    st.session_state.current_question_index = 0
    st.session_state.results = []
    st.session_state.interview_started = False
    st.session_state.interview_completed = False

async def generate_questions_async(job_description: str, difficulty: str, num_questions: int):
    """Generate interview questions asynchronously."""
    return await orchestrator.generate_questions(
        job_description=job_description,
        difficulty=difficulty,
        num_questions=num_questions
    )

async def process_answer_async(question, audio_path, video_path=None):
    """Process answer asynchronously."""
    baseline = None
    if st.session_state.results:
        baseline = {'vocabulary': []}
    
    return await orchestrator.process_answer_with_security(
        question=question,
        audio_path=audio_path,
        video_path=video_path,
        candidate_baseline=baseline
    )

async def generate_summary_async():
    """Generate interview summary asynchronously."""
    return await orchestrator.generate_interview_summary()

async def generate_avatar_async(cv_path, style):
    """Generate avatar asynchronously."""
    return await orchestrator.generate_candidate_avatar(
        cv_path=cv_path,
        style=style if style != "Auto-detect" else None
    )

# ═══════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════
def main():
    # Header
    st.markdown('<div class="main-header">🎯 HireMind - AI Interview System</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <b>Features:</b>
    <ul>
        <li>📝 Intelligent question generation</li>
        <li>🎤 Audio & video recording</li>
        <li>🔒 Real-time cheating detection (AI text, gaze tracking, multi-speaker)</li>
        <li>📊 Comprehensive evaluation</li>
        <li>🎨 CV-based avatar generation</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
     # Show welcome message on first run
    if 'first_run' not in st.session_state:
        st.session_state.first_run = False
        
        with st.expander("👋 Welcome to HireMind!", expanded=True):
            st.markdown("""
            ### 🎯 Getting Started
            
            **HireMind** is an AI-powered interview system with advanced cheating detection.
            
            **Quick Start:**
            1. Go to **📝 Interview** page
            2. Enter a job description and generate questions
            3. Upload audio (required) and video (optional) answers
            4. Get comprehensive analysis with security checks
            
            **Features:**
            - 🤖 AI-powered question generation
            - 🔒 Multi-modal cheating detection
            - 📊 Detailed performance evaluation
            - 🎨 Professional avatar generation
            - 📹 Standalone video analysis
            
            **Need Help?** Check the sidebar help section (❓)
            
            ---
            *Close this message and start your first interview!*
            """)
    # ═══════════════════════════════════════════════════════════
    # SIDEBAR NAVIGATION WITH SYSTEM STATUS
    # ═══════════════════════════════════════════════════════════
    st.sidebar.title("📋 Navigation")
    
    # System status in sidebar
    with st.sidebar.expander("🔧 System Status", expanded=False):
        try:
            status = orchestrator.get_status()
            
            st.write(f"**Framework:** {status.get('framework', 'N/A')}")
            st.write(f"**Model:** {status.get('model', 'N/A')}")
            st.write(f"**Status:** {'🟢 ' if status.get('status') == 'ready' else '🔴 '}{status.get('status', 'unknown')}")
            
            # Interview stats
            stats = status.get('interview_stats', {})
            st.metric("Questions Generated", stats.get('questions_generated', 0))
            st.metric("Answers Processed", stats.get('answers_processed', 0))
            st.metric("Security Flags", stats.get('security_flags', 0))
            
        except Exception as e:
            st.error(f"❌ System status unavailable: {str(e)}")
    
    # Current interview progress
    if st.session_state.interview_started:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Current Interview")
        
        progress = st.session_state.current_question_index / max(len(st.session_state.questions), 1)
        st.sidebar.progress(progress)
        
        st.sidebar.write(f"**Question:** {st.session_state.current_question_index + 1} / {len(st.session_state.questions)}")
        st.sidebar.write(f"**Completed:** {len(st.session_state.results)}")
        
        # Security flags count
        security_flags = len([
            r for r in st.session_state.results 
            if r.get('security_analysis', {}).get('risk_level') in ['MODERATE', 'HIGH']
        ])
        
        if security_flags > 0:
            st.sidebar.warning(f"⚠️ {security_flags} security flag(s)")
        else:
            st.sidebar.success("✅ No security issues")

    # Quick actions
    if st.session_state.results:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ⚡ Quick Actions")
        
        if st.sidebar.button("📥 Quick Export", use_container_width=True):
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'questions': st.session_state.questions,
                'results': st.session_state.results
            }
            
            json_str = json.dumps(export_data, indent=2, default=str)
            
            st.sidebar.download_button(
                label="💾 Download Results",
                data=json_str,
                file_name=f"quick_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    # Page navigation
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Choose a section:",
        ["📝 Interview", "🎨 Avatar Generator", "📊 Statistics", "🔍 Video Analyzer", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    # Help section
    with st.sidebar.expander("❓ Help", expanded=False):
        st.markdown("""
        **Quick Guide:**
        
        1. **Interview**: Generate questions and conduct interviews
        2. **Avatar Generator**: Create professional avatars from CVs
        3. **Statistics**: View interview analytics
        4. **Video Analyzer**: Analyze video recordings separately
        5. **Settings**: Configure system parameters
        
        **Supported Formats:**
        - Audio: WAV, MP3, M4A, OGG
        - Video: MP4, AVI, MOV, WEBM
        - CV: PDF, DOCX, TXT
        """)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**HireMind v2.0**")
    st.sidebar.caption("Powered by LangChain + Ollama")
    
    # ═══════════════════════════════════════════════════════════
    # PAGE ROUTING
    # ═══════════════════════════════════════════════════════════
    if page == "📝 Interview":
        interview_page()
    elif page == "🎨 Avatar Generator":
        avatar_page()
    elif page == "📊 Statistics":
        statistics_page()
    elif page == "🔍 Video Analyzer":
        video_analyzer_page()
    elif page == "⚙️ Settings":
        settings_page()

# ═══════════════════════════════════════════════════════════════
# INTERVIEW PAGE
# ═══════════════════════════════════════════════════════════════

def interview_page():
    st.markdown('<div class="sub-header">📝 Interview Module</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════
    # STEP 1: GENERATE QUESTIONS
    # ═══════════════════════════════════════════════════════════
    if not st.session_state.interview_started:
        st.markdown("### Step 1: Generate Interview Questions")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            job_description = st.text_area(
                "Job Description",
                placeholder="Enter job description or paste job posting...",
                height=200
            )
        
        with col2:
            difficulty = st.selectbox(
                "Difficulty Level",
                ["easy", "medium", "hard"],
                index=1
            )
            
            num_questions = st.slider(
                "Number of Questions",
                min_value=1,
                max_value=10,
                value=3
            )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Generate Questions", type="primary", use_container_width=True):
                if not job_description.strip():
                    st.error("❌ Please enter a job description")
                else:
                    with st.spinner("Generating questions..."):
                        try:
                            questions = asyncio.run(
                                generate_questions_async(
                                    job_description,
                                    difficulty,
                                    num_questions
                                )
                            )
                            
                            if questions:
                                st.session_state.questions = questions
                                st.session_state.interview_started = True
                                st.success(f"✅ Generated {len(questions)} questions!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to generate questions")
                                
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            logger.error(f"Question generation failed: {e}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 2: ANSWER QUESTIONS
    # ═══════════════════════════════════════════════════════════
    elif not st.session_state.interview_completed:
        progress = st.session_state.current_question_index / len(st.session_state.questions)
        st.progress(progress)
        st.write(f"**Question {st.session_state.current_question_index + 1} of {len(st.session_state.questions)}**")
        
        current_question = st.session_state.questions[st.session_state.current_question_index]
        
        st.markdown("### Current Question")
        st.markdown(f'<div class="info-box"><b>{current_question.get("text", "No question")}</b></div>', unsafe_allow_html=True)
        
        st.markdown("### Record Your Answer")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎤 Audio Recording")
            audio_file = st.file_uploader(
                "Upload audio answer (WAV, MP3, M4A, OGG)",
                type=["wav", "mp3", "m4a", "ogg"],
                key=f"audio_{st.session_state.current_question_index}",
                help="Record or upload your answer audio"
            )
            
            if audio_file:
                st.success(f"✅ Audio uploaded: {audio_file.name} ({audio_file.size / 1_000_000:.2f} MB)")
                st.audio(audio_file, format=f'audio/{audio_file.name.split(".")[-1]}')
        
        with col2:
            st.markdown("#### 📹 Video Recording (Optional)")
            video_file = st.file_uploader(
                "Upload video answer (MP4, AVI, MOV, WEBM)",
                type=["mp4", "avi", "mov", "webm"],
                key=f"video_{st.session_state.current_question_index}",
                help="Optional: Upload video for emotion & gaze analysis"
            )
            
            if video_file:
                st.success(f"✅ Video uploaded: {video_file.name} ({video_file.size / 1_000_000:.2f} MB)")
                st.video(video_file)
        
        # Analysis pipeline preview
        if audio_file or video_file:
            with st.expander("📋 Analysis Pipeline", expanded=False):
                analysis_steps = [
                    "🎤 Speech-to-text transcription",
                    "📊 Voice prosody analysis",
                    "🔒 AI text detection",
                    "⏱️ Timing pattern analysis"
                ]
                
                if video_file:
                    analysis_steps.extend([
                        "😊 Facial emotion recognition",
                        "👁️ Eye gaze tracking",
                        "👥 Multi-person detection",
                        "📖 Reading behavior detection"
                    ])
                
                for step in analysis_steps:
                    st.write(f"✓ {step}")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                if not audio_file:
                    st.error("❌ Please upload an audio recording")
                else:
                    with st.spinner("🔄 Processing answer (this may take 30-60 seconds)..."):
                        try:
                            # ========================================
                            # SAVE AUDIO FILE TO TEMP LOCATION
                            # ========================================
                            audio_suffix = os.path.splitext(audio_file.name)[1]
                            with tempfile.NamedTemporaryFile(delete=False, suffix=audio_suffix) as tmp_audio:
                                tmp_audio.write(audio_file.read())
                                audio_path = tmp_audio.name
                            
                            logger.info(f"✅ Audio saved to: {audio_path}")
                            
                            # ========================================
                            # SAVE VIDEO FILE TO TEMP LOCATION (IF PROVIDED)
                            # ========================================
                            video_path = None
                            if video_file:
                                video_suffix = os.path.splitext(video_file.name)[1]
                                with tempfile.NamedTemporaryFile(delete=False, suffix=video_suffix) as tmp_video:
                                    tmp_video.write(video_file.read())
                                    video_path = tmp_video.name
                                
                                logger.info(f"✅ Video saved to: {video_path}")
                                st.info(f"📹 Video analysis enabled: {len(analysis_steps) if video_file else 4} analysis steps")
                            
                            # ========================================
                            # PROCESS ANSWER WITH SECURITY ANALYSIS
                            # ========================================
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            status_text.text("📝 Step 1/5: Transcribing audio...")
                            progress_bar.progress(20)
                            
                            result = asyncio.run(
                                process_answer_async(
                                    current_question,
                                    audio_path,
                                    video_path
                                )
                            )
                            
                            progress_bar.progress(100)
                            status_text.text("✅ Analysis complete!")
                            
                            # ========================================
                            # STORE RESULT
                            # ========================================
                            st.session_state.results.append(result)
                            
                            # ========================================
                            # DISPLAY RESULTS
                            # ========================================
                            st.markdown("---")
                            st.markdown("### 📊 Analysis Results")
                            display_answer_results(result)
                            
                            # ========================================
                            # CLEANUP TEMP FILES
                            # ========================================
                            try:
                                os.unlink(audio_path)
                                logger.info(f"🗑️ Cleaned up audio: {audio_path}")
                            except Exception as e:
                                logger.warning(f"Failed to cleanup audio: {e}")
                            
                            if video_path:
                                try:
                                    os.unlink(video_path)
                                    logger.info(f"🗑️ Cleaned up video: {video_path}")
                                except Exception as e:
                                    logger.warning(f"Failed to cleanup video: {e}")
                            
                            # ========================================
                            # MOVE TO NEXT QUESTION
                            # ========================================
                            st.session_state.current_question_index += 1
                            
                            if st.session_state.current_question_index >= len(st.session_state.questions):
                                st.session_state.interview_completed = True
                                st.balloons()
                                st.success("🎉 Interview Completed!")
                                st.info("Click 'Generate Detailed Summary' below to see final report")
                            else:
                                st.success(f"✅ Moving to question {st.session_state.current_question_index + 1}...")
                                st.info("Click 'Submit Answer' again to continue")
                            
                            # Wait a moment before rerun
                            import time
                            time.sleep(2)
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error processing answer: {str(e)}")
                            logger.error(f"Answer processing failed: {e}")
                            
                            # Show detailed error
                            with st.expander("🔍 Error Details (for debugging)"):
                                import traceback
                                st.code(traceback.format_exc())
    
    # ═══════════════════════════════════════════════════════════
    # STEP 3: GENERATE SUMMARY
    # ═══════════════════════════════════════════════════════════
    else:
        st.markdown("### 🎉 Interview Completed!")
        
        st.markdown(f"""
        <div class="success-box">
        <b>Interview Summary:</b><br>
        ✅ Questions Answered: {len(st.session_state.results)}<br>
        🔒 Security Flags: {len([r for r in st.session_state.results if r.get('security_analysis', {}).get('risk_level') in ['MODERATE', 'HIGH']])}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Generate Detailed Summary", type="primary", use_container_width=True):
            with st.spinner("Generating comprehensive summary..."):
                try:
                    summary = asyncio.run(generate_summary_async())
                    
                    st.markdown("### 📊 Interview Summary Report")
                    st.markdown(summary.get('result', 'Summary generation in progress...'))
                    
                except Exception as e:
                    st.error(f"❌ Error generating summary: {str(e)}")
        
        # Display all results
        st.markdown("### 📝 Detailed Results")
        for i, result in enumerate(st.session_state.results):
            with st.expander(f"Question {i+1} Results", expanded=False):
                display_answer_results(result)
        
        if st.button("🔄 Start New Interview", use_container_width=True):
            reset_interview()
            st.rerun()

def display_answer_results(result):
    """Display answer processing results with separate tabs."""
    
    # Create tabs for different analysis types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Transcript",
        "🔒 Security",
        "😊 Video Analysis",
        "📊 Evaluation",
        "📈 Detailed Metrics"
    ])
    
    # ═══════════════════════════════════════════════════════════
    # TAB 1: TRANSCRIPT
    # ═══════════════════════════════════════════════════════════
    with tab1:
        st.markdown("### 📝 Transcription")
        
        transcript = result.get('transcript', 'No transcript')
        
        if transcript.startswith('[') and 'ERROR' in transcript:
            st.error(transcript)
        elif transcript.startswith('[') and 'Transcription' in transcript:
            st.warning(transcript)
        else:
            st.write(transcript)
            
            # Word count
            word_count = len(transcript.split())
            st.metric("Word Count", word_count)
            
            # Character count
            char_count = len(transcript)
            st.caption(f"Characters: {char_count}")
    
    # ═══════════════════════════════════════════════════════════
    # TAB 2: SECURITY ANALYSIS
    # ═══════════════════════════════════════════════════════════
    with tab2:
        st.markdown("### 🔒 Security & Cheating Detection")
        
        security = result.get('security_analysis', {})
        risk_level = security.get('risk_level', 'UNKNOWN')
        cheating_score = security.get('cheating_score', 0)
        
        # Risk level indicator
        risk_colors = {
            'LOW': 'success',
            'MODERATE': 'warning',
            'HIGH': 'danger',
            'UNKNOWN': 'info'
        }
        risk_color = risk_colors.get(risk_level, 'info')
        risk_emoji = {'LOW': '🟢', 'MODERATE': '🟡', 'HIGH': '🔴', 'UNKNOWN': '⚪'}.get(risk_level, '⚪')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Risk Level",
                f"{risk_emoji} {risk_level}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Cheating Score",
                f"{cheating_score*100:.1f}%",
                delta=None,
                delta_color="inverse"
            )
        
        with col3:
            num_indicators = len(security.get('indicators', []))
            st.metric(
                "Indicators",
                num_indicators,
                delta=None,
                delta_color="inverse"
            )
        
        # Detailed indicators
        if security.get('indicators'):
            st.markdown("#### 🔍 Security Indicators Detected")
            
            for idx, indicator in enumerate(security['indicators'], 1):
                with st.expander(f"Indicator {idx}: {indicator['type'].replace('_', ' ').title()}", expanded=idx==1):
                    st.write(f"**Type:** {indicator['type']}")
                    st.write(f"**Severity:** {indicator.get('severity', 'medium')}")
                    st.write(f"**Evidence:**")
                    st.info(indicator['evidence'])
        else:
            st.success("✅ No security concerns detected")
        
        # Summary
        st.markdown("#### 📋 Summary")
        st.write(security.get('summary', 'No summary available'))
    
    # ═══════════════════════════════════════════════════════════
    # TAB 3: VIDEO ANALYSIS (NEW!)
    # ═══════════════════════════════════════════════════════════
    with tab3:
        st.markdown("### 📹 Video Analysis")
        
        emotion_analysis = result.get('emotion_analysis', {})
        
        if not emotion_analysis or emotion_analysis.get('result') == 'Skipped - transcription failed':
            st.info("📹 No video was uploaded for this answer")
            st.write("Video analysis includes:")
            st.write("- 😊 Facial emotion recognition")
            st.write("- 👁️ Eye gaze tracking")
            st.write("- 👥 Multi-person detection")
            st.write("- 📖 Reading behavior detection")
        else:
            # Emotion timeline
            if 'emotion_timeline' in emotion_analysis:
                st.markdown("#### 😊 Emotion Timeline")
                timeline = emotion_analysis['emotion_timeline']
                
                if timeline:
                    # Show emotion distribution
                    emotion_counts = {}
                    for frame in timeline:
                        emotion = frame.get('dominant_emotion', 'unknown')
                        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                    
                    st.bar_chart(emotion_counts)
                    
                    st.caption(f"Analyzed {len(timeline)} frames")
                else:
                    st.info("No emotion data available")
            
            # Gaze analysis
            if 'gaze_analysis' in emotion_analysis:
                st.markdown("#### 👁️ Gaze Tracking")
                gaze = emotion_analysis['gaze_analysis']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    camera_focus = gaze.get('camera_focus_ratio', 0)
                    st.metric("Camera Focus", f"{camera_focus*100:.1f}%")
                
                with col2:
                    reading_detected = gaze.get('reading_pattern_detected', False)
                    st.metric("Reading Pattern", "Yes" if reading_detected else "No")
                
                if reading_detected:
                    st.warning("⚠️ Reading pattern detected - candidate may be reading answers")
            
            # Face verification
            if 'face_verification' in emotion_analysis:
                st.markdown("#### 👥 Face Verification")
                face_verify = emotion_analysis['face_verification']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    num_faces = face_verify.get('num_unique_faces', 0)
                    st.metric("Unique Faces", num_faces)
                
                with col2:
                    same_person = face_verify.get('same_person_throughout', True)
                    st.metric("Same Person", "Yes" if same_person else "No")
                
                if num_faces > 1:
                    st.error("🚨 Multiple faces detected - potential cheating!")
            
            # Raw result
            with st.expander("📄 Raw Video Analysis"):
                st.json(emotion_analysis)
    
    # ═══════════════════════════════════════════════════════════
    # TAB 4: EVALUATION
    # ═══════════════════════════════════════════════════════════
    with tab4:
        st.markdown("### 📊 Answer Evaluation")
        
        evaluation = result.get('evaluation', {})
        
        # Overall score
        overall_score = evaluation.get('overall_score', 'N/A')
        
        if isinstance(overall_score, (int, float)):
            st.metric(
                "Overall Score",
                f"{overall_score}/100",
                delta=None
            )
            
            # Progress bar
            st.progress(overall_score / 100)
        else:
            st.metric("Overall Score", overall_score)
        
        # Strengths
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Strengths")
            strengths = evaluation.get('strengths', 'N/A')
            if isinstance(strengths, list):
                for strength in strengths:
                    st.write(f"- {strength}")
            else:
                st.write(strengths)
        
        # Areas for improvement
        with col2:
            st.markdown("#### 📈 Areas for Improvement")
            improvements = evaluation.get('areas_for_improvement', 'N/A')
            if isinstance(improvements, list):
                for improvement in improvements:
                    st.write(f"- {improvement}")
            else:
                st.write(improvements)
        
        # Full evaluation text
        if 'result' in evaluation:
            with st.expander("📄 Full Evaluation"):
                st.write(evaluation['result'])
    
    # ═══════════════════════════════════════════════════════════
    # TAB 5: DETAILED METRICS
    # ═══════════════════════════════════════════════════════════
    with tab5:
        st.markdown("### 📈 Detailed Metrics")
        
        # Prosody analysis
        prosody = result.get('prosody_analysis', {})
        if prosody and prosody.get('result'):
            st.markdown("#### 🎵 Voice Prosody")
            st.write(prosody.get('result', 'N/A'))
        
        # Timestamps
        if 'timestamp' in result:
            st.markdown("#### ⏰ Timing")
            st.write(f"Processing time: {result['timestamp']:.2f}s")
        
        # Raw data
        with st.expander("🔧 Raw Response Data"):
            st.json(result)


# ═══════════════════════════════════════════════════════════════
# AVATAR GENERATOR PAGE
# ═══════════════════════════════════════════════════════════════

def avatar_page():
    st.markdown('<div class="sub-header">🎨 Avatar Generator</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Generate professional avatars from CV files using AI-powered image generation.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload CV")
        cv_file = st.file_uploader(
            "Upload CV (PDF, DOCX, TXT)",
            type=["pdf", "docx", "doc", "txt"]
        )
        
        style = st.selectbox(
            "Visual Style",
            ["Auto-detect", "tech-professional", "business-formal", 
             "creative-artistic", "academic-researcher"]
        )
        
        if st.button("🎨 Generate Avatar", type="primary", use_container_width=True):
            if not cv_file:
                st.error("❌ Please upload a CV file")
            else:
                with st.spinner("Generating avatar (this may take a minute)..."):
                    try:
                        # Save CV temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cv_file.name)[1]) as tmp_cv:
                            tmp_cv.write(cv_file.read())
                            cv_path = tmp_cv.name
                        
                        # Generate avatar
                        result = asyncio.run(
                            generate_avatar_async(cv_path, style)
                        )
                        
                        if 'error' in result:
                            st.error(f"❌ Error: {result['error']}")
                        else:
                            avatar_data = result.get('result', {})
                            image_path = avatar_data.get('image_path')
                            
                            if image_path and os.path.exists(image_path):
                                st.session_state.avatar_result = avatar_data
                                st.success("✅ Avatar generated successfully!")
                                st.rerun()
                            else:
                                st.warning("⚠️ Avatar generated (placeholder mode)")
                        
                        # Cleanup
                        try:
                            os.unlink(cv_path)
                        except:
                            pass
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        logger.error(f"Avatar generation failed: {e}")
    
    with col2:
        st.markdown("### Generated Avatar")
        
        if 'avatar_result' in st.session_state:
            avatar_data = st.session_state.avatar_result
            image_path = avatar_data.get('image_path')
            
            if image_path and os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
                
                metadata = avatar_data.get('metadata', {})
                
                st.markdown(f"""
                <div class="info-box">
                <b>Avatar Details:</b><br>
                👤 Name: {metadata.get('name', 'N/A')}<br>
                💼 Role: {metadata.get('role', 'N/A')}<br>
                🏢 Domain: {metadata.get('domain', 'N/A')}<br>
                📊 Seniority: {metadata.get('seniority', 'N/A')}<br>
                🎨 Style: {avatar_data.get('style', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Upload a CV and click 'Generate Avatar' to see results")

# ═══════════════════════════════════════════════════════════════
# STATISTICS PAGE
# ═══════════════════════════════════════════════════════════════

def statistics_page():
    st.markdown('<div class="sub-header">📊 Interview Statistics</div>', unsafe_allow_html=True)
    
    if not st.session_state.results:
        st.info("No interview data available. Complete an interview first.")
        return
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Questions", len(st.session_state.questions))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Answers", len(st.session_state.results))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        security_flags = len([
            r for r in st.session_state.results 
            if r.get('security_analysis', {}).get('risk_level') in ['MODERATE', 'HIGH']
        ])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Security Flags", security_flags)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        avg_score = sum([
            r.get('evaluation', {}).get('overall_score', 0) 
            for r in st.session_state.results
        ]) / max(len(st.session_state.results), 1)
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Score", f"{avg_score:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk distribution
    st.markdown("### 🔒 Security Risk Distribution")
    risk_counts = {'LOW': 0, 'MODERATE': 0, 'HIGH': 0}
    for result in st.session_state.results:
        risk_level = result.get('security_analysis', {}).get('risk_level', 'LOW')
        risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"🟢 **Low Risk:** {risk_counts['LOW']}")
    with col2:
        st.markdown(f"🟡 **Moderate Risk:** {risk_counts['MODERATE']}")
    with col3:
        st.markdown(f"🔴 **High Risk:** {risk_counts['HIGH']}")

# ═══════════════════════════════════════════════════════════════
# VIDEO ANALYZER PAGE -
# ═══════════════════════════════════════════════════════════════

def video_analyzer_page():
    """Standalone video analysis page for detailed behavioral analysis."""
    st.markdown('<div class="sub-header">🔍 Video Analyzer</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Analyze interview videos independently for:
    - 😊 Emotion detection
    - 👁️ Gaze tracking
    - 👥 Face verification
    - 📖 Reading behavior detection
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload Video")
        
        video_file = st.file_uploader(
            "Upload interview video (MP4, AVI, MOV, WEBM)",
            type=["mp4", "avi", "mov", "webm"],
            key="standalone_video"
        )
        
        if video_file:
            st.success(f"✅ Video uploaded: {video_file.name} ({video_file.size / 1_000_000:.2f} MB)")
            st.video(video_file)
            
            # Analysis options
            st.markdown("### Analysis Options")
            
            analyze_emotions = st.checkbox("😊 Emotion Recognition", value=True)
            analyze_gaze = st.checkbox("👁️ Gaze Tracking", value=True)
            analyze_faces = st.checkbox("👥 Face Verification", value=True)
            analyze_reading = st.checkbox("📖 Reading Detection", value=True)
            
            # Frame sampling rate
            frame_rate = st.slider(
                "Frame Sampling Rate (fps)",
                min_value=1,
                max_value=30,
                value=5,
                help="Higher = more detailed but slower"
            )
            
            if st.button("🔍 Analyze Video", type="primary", use_container_width=True):
                with st.spinner("Analyzing video... This may take a few minutes"):
                    try:
                        # Save video temporarily
                        video_suffix = os.path.splitext(video_file.name)[1]
                        with tempfile.NamedTemporaryFile(delete=False, suffix=video_suffix) as tmp_video:
                            tmp_video.write(video_file.read())
                            video_path = tmp_video.name
                        
                        logger.info(f"✅ Video saved to: {video_path}")
                        
                        # Import video analyzer
                        from services.cheating_detector.video_analyzer import video_analyzer
                        
                        # Analyze video
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("📹 Processing video frames...")
                        progress_bar.progress(25)
                        
                        result = video_analyzer.analyze_video(
                            video_path=video_path,
                            sample_rate=frame_rate
                        )
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        
                        # Store result
                        st.session_state.video_analysis_result = result
                        
                        # Cleanup
                        try:
                            os.unlink(video_path)
                            logger.info(f"🗑️ Cleaned up video: {video_path}")
                        except Exception as e:
                            logger.warning(f"Failed to cleanup video: {e}")
                        
                        st.success("✅ Video analysis completed!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error analyzing video: {str(e)}")
                        logger.error(f"Video analysis failed: {e}")
                        
                        with st.expander("🔍 Error Details"):
                            import traceback
                            st.code(traceback.format_exc())
    
    with col2:
        st.markdown("### Analysis Results")
        
        if 'video_analysis_result' in st.session_state:
            result = st.session_state.video_analysis_result
            
            # Create tabs for different analyses
            tab1, tab2, tab3, tab4 = st.tabs([
                "😊 Emotions",
                "👁️ Gaze",
                "👥 Faces",
                "📊 Summary"
            ])
            
            # ═══════════════════════════════════════════════
            # TAB 1: EMOTION ANALYSIS
            # ═══════════════════════════════════════════════
            with tab1:
                st.markdown("#### 😊 Emotion Distribution")
                
                emotion_timeline = result.get('emotion_timeline', [])
                
                if emotion_timeline:
                    # Count emotions
                    emotion_counts = {}
                    for frame in emotion_timeline:
                        emotion = frame.get('dominant_emotion', 'unknown')
                        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                    
                    # Display chart
                    st.bar_chart(emotion_counts)
                    
                    # Statistics
                    total_frames = len(emotion_timeline)
                    st.write(f"**Total Frames Analyzed:** {total_frames}")
                    
                    # Most common emotion
                    if emotion_counts:
                        most_common = max(emotion_counts.items(), key=lambda x: x[1])
                        st.metric(
                            "Most Common Emotion",
                            most_common[0].title(),
                            f"{most_common[1]/total_frames*100:.1f}% of time"
                        )
                    
                    # Timeline visualization
                    with st.expander("📅 Emotion Timeline"):
                        for i, frame in enumerate(emotion_timeline[:20]):  # Show first 20
                            timestamp = frame.get('timestamp', i)
                            emotion = frame.get('dominant_emotion', 'unknown')
                            confidence = frame.get('confidence', 0)
                            
                            st.write(f"**{timestamp:.2f}s:** {emotion.title()} ({confidence*100:.1f}%)")
                else:
                    st.info("No emotion data available")
            
            # ═══════════════════════════════════════════════
            # TAB 2: GAZE ANALYSIS
            # ═══════════════════════════════════════════════
            with tab2:
                st.markdown("#### 👁️ Gaze Tracking Results")
                
                gaze_analysis = result.get('gaze_analysis', {})
                
                if gaze_analysis:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        camera_focus = gaze_analysis.get('camera_focus_ratio', 0)
                        st.metric(
                            "Camera Focus",
                            f"{camera_focus*100:.1f}%",
                            help="Percentage of time looking at camera"
                        )
                    
                    with col2:
                        avg_deviation = gaze_analysis.get('average_gaze_deviation', 0)
                        st.metric(
                            "Avg Gaze Deviation",
                            f"{avg_deviation:.1f}°",
                            help="Average angular deviation from camera"
                        )
                    
                    # Reading pattern detection
                    reading_detected = gaze_analysis.get('reading_pattern_detected', False)
                    
                    if reading_detected:
                        st.warning("⚠️ **Reading Pattern Detected**")
                        st.write("Candidate may be reading from external sources")
                        
                        reading_segments = gaze_analysis.get('reading_segments', [])
                        if reading_segments:
                            st.write(f"**Detected {len(reading_segments)} reading segment(s):**")
                            for segment in reading_segments:
                                st.write(f"- {segment['start']:.1f}s - {segment['end']:.1f}s")
                    else:
                        st.success("✅ No reading patterns detected")
                    
                    # Gaze heatmap (if available)
                    if 'gaze_positions' in gaze_analysis:
                        with st.expander("🔥 Gaze Heatmap Data"):
                            positions = gaze_analysis['gaze_positions']
                            st.write(f"Tracked {len(positions)} gaze positions")
                else:
                    st.info("No gaze tracking data available")
            
            # ═══════════════════════════════════════════════
            # TAB 3: FACE VERIFICATION
            # ═══════════════════════════════════════════════
            with tab3:
                st.markdown("#### 👥 Face Verification")
                
                face_verification = result.get('face_verification', {})
                
                if face_verification:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        num_faces = face_verification.get('num_unique_faces', 0)
                        st.metric("Unique Faces", num_faces)
                    
                    with col2:
                        same_person = face_verification.get('same_person_throughout', True)
                        st.metric(
                            "Same Person",
                            "Yes" if same_person else "No",
                            delta_color="off"
                        )
                    
                    with col3:
                        face_detected_ratio = face_verification.get('face_detected_ratio', 0)
                        st.metric(
                            "Face Visible",
                            f"{face_detected_ratio*100:.1f}%"
                        )
                    
                    # Multiple faces warning
                    if num_faces > 1:
                        st.error("🚨 **Multiple Faces Detected - Potential Cheating!**")
                        st.write("This may indicate unauthorized assistance during the interview")
                    elif not same_person:
                        st.warning("⚠️ **Different Person Detected**")
                        st.write("Face identity changed during interview")
                    else:
                        st.success("✅ Single person verified throughout interview")
                    
                    # Face detection timeline
                    if 'face_timeline' in face_verification:
                        with st.expander("📅 Face Detection Timeline"):
                            timeline = face_verification['face_timeline']
                            for entry in timeline[:20]:
                                st.write(f"**{entry['timestamp']:.2f}s:** {entry['num_faces']} face(s)")
                else:
                    st.info("No face verification data available")
            
            # ═══════════════════════════════════════════════
            # TAB 4: SUMMARY
            # ═══════════════════════════════════════════════
            with tab4:
                st.markdown("#### 📊 Analysis Summary")
                
                summary = result.get('summary', {})
                
                if summary:
                    # Overall verdict
                    suspicious = summary.get('suspicious_behavior', False)
                    
                    if suspicious:
                        st.error("🔴 **Suspicious Behavior Detected**")
                    else:
                        st.success("🟢 **No Suspicious Behavior Detected**")
                    
                    # Key findings
                    st.markdown("**Key Findings:**")
                    findings = summary.get('findings', [])
                    
                    if findings:
                        for finding in findings:
                            st.write(f"- {finding}")
                    else:
                        st.write("- No significant findings")
                    
                    # Confidence scores
                    st.markdown("**Confidence Scores:**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        emotion_confidence = summary.get('emotion_confidence', 0)
                        st.metric("Emotion Detection", f"{emotion_confidence*100:.1f}%")
                    
                    with col2:
                        gaze_confidence = summary.get('gaze_confidence', 0)
                        st.metric("Gaze Tracking", f"{gaze_confidence*100:.1f}%")
                else:
                    st.write("No summary available")
                
                # Export results
                if st.button("📥 Export Results as JSON"):
                    import json
                    
                    json_str = json.dumps(result, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_str,
                        file_name=f"video_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        else:
            st.info("👆 Upload a video and click 'Analyze Video' to see results")
            
            # Example use cases
            with st.expander("💡 Use Cases"):
                st.markdown("""
                **When to use Video Analyzer:**
                
                1. **Post-Interview Review**: Analyze recorded interviews in detail
                2. **Suspicious Behavior Investigation**: Deep dive into flagged interviews
                3. **Training**: Review candidate body language and behavior
                4. **Quality Assurance**: Verify interview integrity
                5. **Research**: Study behavioral patterns across multiple interviews
                """)


# ═══════════════════════════════════════════════════════════════
# SETTINGS PAGE 
# ═══════════════════════════════════════════════════════════════

def settings_page():
    """System settings and configuration page."""
    st.markdown('<div class="sub-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    # Initialize settings in session state if not exists
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'model_name': 'phi4-mini',
            'temperature': 0.7,
            'max_tokens': 2000,
            'enable_video_analysis': True,
            'enable_ai_detection': True,
            'frame_sample_rate': 5,
            'audio_quality': 'high',
            'save_recordings': False,
            'export_format': 'json'
        }
    
    # Create tabs for different settings
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 Model Settings",
        "📹 Video Analysis",
        "🔒 Security",
        "💾 Data & Export"
    ])
    
    # ═══════════════════════════════════════════════════════════
    # TAB 1: MODEL SETTINGS
    # ═══════════════════════════════════════════════════════════
    with tab1:
        st.markdown("### 🤖 Language Model Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            model_name = st.selectbox(
                "Model",
                ["phi4-mini", "llama3", "mistral", "mixtral"],
                index=0,
                help="Select the LLM model to use"
            )
            st.session_state.settings['model_name'] = model_name
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.settings['temperature'],
                step=0.1,
                help="Higher = more creative, Lower = more deterministic"
            )
            st.session_state.settings['temperature'] = temperature
        
        with col2:
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=100,
                max_value=8000,
                value=st.session_state.settings['max_tokens'],
                step=100,
                help="Maximum length of generated responses"
            )
            st.session_state.settings['max_tokens'] = max_tokens
            
            st.markdown("**Current Model Info:**")
            try:
                status = orchestrator.get_status()
                st.info(f"Framework: {status.get('framework', 'N/A')}")
                st.info(f"Active Model: {status.get('model', 'N/A')}")
            except:
                st.warning("Unable to fetch model status")
        
        if st.button("💾 Save Model Settings", use_container_width=True):
            st.success("✅ Model settings saved!")
            st.info("Note: Restart the app to apply model changes")
    
    # ═══════════════════════════════════════════════════════════
    # TAB 2: VIDEO ANALYSIS SETTINGS
    # ═══════════════════════════════════════════════════════════
    with tab2:
        st.markdown("### 📹 Video Analysis Configuration")
        
        enable_video = st.checkbox(
            "Enable Video Analysis",
            value=st.session_state.settings['enable_video_analysis'],
            help="Process video for emotion detection and gaze tracking"
        )
        st.session_state.settings['enable_video_analysis'] = enable_video
        
        if enable_video:
            col1, col2 = st.columns(2)
            
            with col1:
                frame_rate = st.slider(
                    "Frame Sampling Rate (fps)",
                    min_value=1,
                    max_value=30,
                    value=st.session_state.settings['frame_sample_rate'],
                    help="Higher = more detailed but slower"
                )
                st.session_state.settings['frame_sample_rate'] = frame_rate
                
                st.info(f"Processing every {1/frame_rate:.2f} seconds")
            
            with col2:
                st.markdown("**Enabled Analyses:**")
                st.write("✓ Emotion detection")
                st.write("✓ Gaze tracking")
                st.write("✓ Face verification")
                st.write("✓ Reading detection")
                
                processing_time = frame_rate * 0.5  # Rough estimate
                st.caption(f"Estimated processing time: ~{processing_time:.0f}s per minute of video")
        else:
            st.warning("⚠️ Video analysis is disabled. Only audio will be processed.")
        
        if st.button("💾 Save Video Settings", use_container_width=True):
            st.success("✅ Video analysis settings saved!")
    
    # ═══════════════════════════════════════════════════════════
    # TAB 3: SECURITY SETTINGS
    # ═══════════════════════════════════════════════════════════
    with tab3:
        st.markdown("### 🔒 Security & Cheating Detection")
        
        enable_ai_detection = st.checkbox(
            "Enable AI Text Detection",
            value=st.session_state.settings['enable_ai_detection'],
            help="Check for ChatGPT/AI-generated responses"
        )
        st.session_state.settings['enable_ai_detection'] = enable_ai_detection
        
        st.markdown("**Detection Methods:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Text Analysis")
            st.write("✓ Perplexity checking")
            st.write("✓ Sentence uniformity")
            st.write("✓ Vocabulary formality")
            st.write("✓ Timing patterns")
        
        with col2:
            st.markdown("##### Behavioral Analysis")
            st.write("✓ Multi-speaker detection")
            st.write("✓ Gaze tracking")
            st.write("✓ Reading patterns")
            st.write("✓ Face verification")
        
        st.markdown("---")
        
        st.markdown("**Risk Thresholds:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Low Risk", "< 30%", delta="Safe", delta_color="normal")
        
        with col2:
            st.metric("Moderate Risk", "30-60%", delta="Review", delta_color="off")
        
        with col3:
            st.metric("High Risk", "> 60%", delta="Flag", delta_color="inverse")
        
        if st.button("💾 Save Security Settings", use_container_width=True):
            st.success("✅ Security settings saved!")
    
    # ═══════════════════════════════════════════════════════════
    # TAB 4: DATA & EXPORT SETTINGS
    # ═══════════════════════════════════════════════════════════
    with tab4:
        st.markdown("### 💾 Data Management & Export")
        
        save_recordings = st.checkbox(
            "Save Recordings Permanently",
            value=st.session_state.settings['save_recordings'],
            help="Keep audio/video files after analysis (for auditing)"
        )
        st.session_state.settings['save_recordings'] = save_recordings
        
        export_format = st.selectbox(
            "Export Format",
            ["json", "csv", "pdf"],
            index=0,
            help="Format for exporting interview results"
        )
        st.session_state.settings['export_format'] = export_format
        
        st.markdown("---")
        
        st.markdown("### 📥 Export Interview Data")
        
        if st.session_state.results:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Available Data:**")
                st.write(f"- {len(st.session_state.questions)} Questions")
                st.write(f"- {len(st.session_state.results)} Answers")
                st.write(f"- {len([r for r in st.session_state.results if r.get('security_analysis')])} Security Reports")
            
            with col2:
                if st.button("📥 Export as JSON", use_container_width=True):
                    export_data = {
                        'interview_metadata': {
                            'timestamp': datetime.now().isoformat(),
                            'num_questions': len(st.session_state.questions),
                            'num_answers': len(st.session_state.results),
                            'settings': st.session_state.settings
                        },
                        'questions': st.session_state.questions,
                        'results': st.session_state.results
                    }
                    
                    json_str = json.dumps(export_data, indent=2, default=str)
                    
                    st.download_button(
                        label="💾 Download JSON",
                        data=json_str,
                        file_name=f"interview_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                if st.button("📊 Export as CSV", use_container_width=True):
                    import csv
                    import io
                    
                    output = io.StringIO()
                    writer = csv.writer(output)
                    
                    # Header
                    writer.writerow([
                        'Question #',
                        'Question Text',
                        'Transcript',
                        'Risk Level',
                        'Cheating Score',
                        'Overall Score',
                        'Timestamp'
                    ])
                    
                    # Data rows
                    for i, result in enumerate(st.session_state.results, 1):
                        question = result.get('question', {})
                        security = result.get('security_analysis', {})
                        evaluation = result.get('evaluation', {})
                        
                        writer.writerow([
                            i,
                            question.get('text', 'N/A'),
                            result.get('transcript', 'N/A')[:100] + '...',
                            security.get('risk_level', 'UNKNOWN'),
                            f"{security.get('cheating_score', 0)*100:.1f}%",
                            evaluation.get('overall_score', 'N/A'),
                            result.get('timestamp', 'N/A')
                        ])
                    
                    csv_data = output.getvalue()
                    
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv_data,
                        file_name=f"interview_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        else:
            st.info("No interview data available to export. Complete an interview first.")
        
        st.markdown("---")
        
        st.markdown("### 🗑️ Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Clear Current Session", use_container_width=True):
                if st.button("⚠️ Confirm Clear", type="primary"):
                    reset_interview()
                    st.success("✅ Session data cleared!")
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Delete All Data", use_container_width=True):
                if st.button("⚠️⚠️ CONFIRM DELETE ALL", type="primary"):
                    st.session_state.clear()
                    st.success("✅ All data deleted!")
                    st.rerun()
        
        st.markdown("---")
        
        if st.button("💾 Save All Settings", type="primary", use_container_width=True):
            st.success("✅ All settings saved successfully!")
            st.balloons()

# ═══════════════════════════════════════════════════════════════
# RUN APP
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()