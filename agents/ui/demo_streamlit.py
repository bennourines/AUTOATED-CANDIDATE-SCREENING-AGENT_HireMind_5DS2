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
    
    # Sidebar Navigation
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.radio(
        "Choose a section:",
        ["📝 Interview", "🎨 Avatar Generator", "📊 Statistics"]
    )
    
    if page == "📝 Interview":
        interview_page()
    elif page == "🎨 Avatar Generator":
        avatar_page()
    elif page == "📊 Statistics":
        statistics_page()

# ═══════════════════════════════════════════════════════════════
# INTERVIEW PAGE
# ═══════════════════════════════════════════════════════════════

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

def display_answer_results(result):
    """Display answer processing results."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Transcript")
        st.write(result.get('transcript', 'No transcript'))
        
        st.markdown("#### 🔒 Security Analysis")
        security = result.get('security_analysis', {})
        risk_level = security.get('risk_level', 'UNKNOWN')
        
        risk_colors = {
            'LOW': 'success',
            'MODERATE': 'warning',
            'HIGH': 'danger'
        }
        risk_color = risk_colors.get(risk_level, 'info')
        
        risk_emoji = {'LOW': '🟢', 'MODERATE': '🟡', 'HIGH': '🔴'}.get(risk_level, '⚪')
        
        st.markdown(f"""
        <div class="{risk_color}-box">
        <b>{risk_emoji} Risk Level: {risk_level}</b><br>
        Cheating Score: {security.get('cheating_score', 0)*100:.1f}%<br>
        Indicators Detected: {len(security.get('indicators', []))}
        </div>
        """, unsafe_allow_html=True)
        
        if security.get('indicators'):
            st.markdown("**Details:**")
            for ind in security['indicators'][:3]:
                st.write(f"- **{ind['type']}**: {ind['evidence'][:100]}...")
    
    with col2:
        st.markdown("#### 📊 Evaluation")
        evaluation = result.get('evaluation', {})
        
        st.metric("Overall Score", evaluation.get('overall_score', 'N/A'))
        
        st.markdown("**Strengths:**")
        st.write(evaluation.get('strengths', 'N/A'))
        
        st.markdown("**Areas for Improvement:**")
        st.write(evaluation.get('areas_for_improvement', 'N/A'))

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
# RUN APP
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()