# In app/utils.py
print("--- RUNNING API-ONLY UTILS MODULE (WITH OPENAI FIX) ---")

import os
import re
import requests
from typing import List
from io import BytesIO
import docx
import pypdf
import os
from openai import OpenAI # <-- IMPORT OPENAI

# --- Setup ---
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") # <-- GET OPENAI KEY
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# --- Initialize OpenAI Client ---
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Hugging Face API URLs ---
QA_API_URL = "https://api-inference.huggingface.co/models/google-bert/bert-large-uncased-whole-word-masking-finetuned-squad"
SUMMARIZATION_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# --- Skill Lists ---
TECH_SKILLS = ["Python", "Java", "C++", "SQL", "AWS", "Docker", "Kubernetes", "React", "Node.js", "Django", "Flask", "TensorFlow", "Git", "Linux"]
SOFT_SKILLS = ["Management", "Leadership", "Communication", "Problem Solving", "Teamwork", "Project Management", "Agile", "Scrum", "Client Relations", "Coordination"]

# --- Reusable API Functions ---
def query_api(api_url, payload, timeout=25):
    # This function remains for the other Hugging Face calls
    try:
        response = requests.post(api_url, headers=HEADERS, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call to {api_url} failed: {e}")
        return {"error": str(e)}

# =============================================================
# THE NEW, RELIABLE OPENAI-POWERED LLM FUNCTION
# =============================================================
def call_llm(prompt: str) -> str:
    """A generic function to call the OpenAI GPT-3.5-Turbo model."""
    if not OPENAI_API_KEY:
        return "Error: OpenAI API key is not configured."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=250
        )
        content = response.choices[0].message.content
        return content.strip()
        
    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        return f"Error: The AI service failed. Details: {e}"

# --- Other AI Functions (Unchanged) ---
def generate_summary(text: str) -> str:
    prompt = f"Summarize the following resume's 'Career Summary' section in one or two sentences. Do not add any information not present in that section.\n\nResume Text:\n\"\"\"{text[:1024]}\"\"\""
    output = query_api(SUMMARIZATION_API_URL, {"inputs": prompt})
    if "error" in output:
        print(f"AI summary error: {output.get('error')}")
        return "AI summary is being generated. Please wait."
    return output[0].get('summary_text', "Could not generate summary.")

def ask_question(context: str, question: str) -> str:
    output = query_api(QA_API_URL, {"inputs": {"question": question, "context": context}})
    if "error" in output: return None
    return output.get('answer') if output.get('score', 0) > 0.1 else None

# --- Main Parsing Function (Unchanged) ---
def parse_resume(file_bytes: bytes, filename: str) -> dict:
    # ... (This function is unchanged)
    raw_text = ""
    try:
        if filename.endswith(".pdf"):
            reader = pypdf.PdfReader(BytesIO(file_bytes))
            raw_text = "".join(page.extract_text() or "" for page in reader.pages)
        elif filename.endswith(".docx"):
            raw_text = "\n".join([p.text for p in docx.Document(BytesIO(file_bytes)).paragraphs])
        else: return {"error": "Unsupported file type."}
    except Exception as e:
        return {"error": f"Could not read file content: {e}"}
    context = raw_text[:4000]
    if not context: return {"error": "Could not extract any text from the document."}
    name = ask_question(context, "What is the candidate's full name?")
    if not name:
        name_match = re.search(r"^([A-Z][a-z'’]+)\s([A-Z]\.\s)?([A-Z][a-z'’]+)", context.strip())
        name = name_match.group(0) if name_match else None
    email = ask_question(context, "What is the email address?")
    if not email:
        email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", context)
        email = email_match.group(0) if email_match else None
    phone = ask_question(context, "What is the phone number?")
    education = ask_question(context, "What is the name of the university?")
    location = ask_question(context, "What city and state is listed in the address?")
    experience = ask_question(context, "How many years of experience are mentioned in the career summary?")
    current_title = ask_question(context, "What is the job title listed for the most recent employment history date?")
    all_skills = TECH_SKILLS + SOFT_SKILLS
    skills_list = {skill for skill in all_skills if re.search(r"\b" + re.escape(skill) + r"\b", raw_text, re.IGNORECASE)}
    summary = generate_summary(raw_text)
    return {
        "full_name": name, "email": email, "phone": phone,
        "location": location, "current_title": current_title, "experience": experience,
        "skills": sorted(list(skills_list)),
        "education": education, "professional_summary": summary, "raw_text": raw_text[:2000]
    }

# --- This function for recruiter insights now also uses call_llm ---
def generate_candidate_insights(resume_text: str, job_description: str) -> dict:
    prompt = f"""
    You are an expert technical recruiter. Analyze the following resume against the job description.
    Based ONLY on the information provided, list exactly 3 strengths and 1 potential consideration (weakness).
    Format your response as a JSON object with two keys: "strengths" (a list of strings) and "considerations" (a list of strings).

    Job Description:
    \"\"\"{job_description[:1500]}\"\"\"

    Resume Text:
    \"\"\"{resume_text[:2500]}\"\"\"
    
    JSON Response:
    """
    # This now uses the reliable OpenAI call
    response_text = call_llm(prompt)
    try:
        import json
        insights = json.loads(response_text)
        return insights
    except:
        return {"strengths": ["AI analysis failed to produce valid JSON."], "considerations": []}

# --- Unchanged Function ---
def calculate_match_score(candidate_skills: List[str], job_skills: List[str]) -> int:
    if not job_skills or not candidate_skills: return 0
    common_skills = set(c.lower() for c in candidate_skills) & set(j.lower() for j in job_skills)
    return int((len(common_skills) / len(job_skills)) * 100)