# In app/utils.py
print("--- RUNNING utils.py (WITH ADVANCED LAYOUTLM PARSER) ---")

import os
import re
import requests
from typing import List
from io import BytesIO
from PIL import Image
import pypdfium2 as pdfium # More robust PDF handling for images

# NEW IMPORTS FOR THE ADVANCED MODEL
from transformers import pipeline

# --- Setup ---
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
SUMMARIZATION_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

# Initialize the advanced Document Question Answering pipeline
# This will download the model the first time it's run (can take a few minutes)
try:
    print("Loading LayoutLM document parsing model...")
    doc_qa_pipeline = pipeline(
        "document-question-answering",
        model="impira/layoutlm-document-qa"
    )
    print("LayoutLM model loaded successfully.")
except Exception as e:
    print(f"Failed to load LayoutLM model: {e}")
    doc_qa_pipeline = None

# --- Reusable AI Functions ---

def query_huggingface_api(api_url, payload, headers):
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

def generate_summary(text: str) -> str:
    # This function remains the same, using the free summarization API
    if not HUGGINGFACE_API_KEY:
        return "Hugging Face API key not configured."
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    try:
        output = query_huggingface_api(SUMMARIZATION_API_URL, {
            "inputs": text[:1024],
            "parameters": {"min_length": 30, "max_length": 100}
        })
        if "error" in output:
            return f"AI summary error: {output['error']}"
        return output[0]['summary_text']
    except Exception as e:
        return f"AI summary request failed: {e}"

def extract_from_document(image, question: str) -> str:
    """Uses the LayoutLM model to answer a question about a document image."""
    if not doc_qa_pipeline:
        return None
    try:
        result = doc_qa_pipeline(image=image, question=question)
        # The model returns a list of answers, we take the best one
        return result[0]['answer'] if result else None
    except Exception as e:
        print(f"Error during document QA for question '{question}': {e}")
        return None

# The main parsing function - completely rewritten
def parse_resume(file_bytes: bytes, filename: str) -> dict:
    print("--- INSIDE THE ADVANCED LAYOUTLM PARSE_RESUME FUNCTION ---")
    
    # This model works on IMAGES. So we must convert the PDF to an image.
    try:
        if filename.endswith(".pdf"):
            # Convert PDF to a list of PIL Images
            images = pdfium.render_pdf_to_pil(file_bytes)
            first_page_image = images[0]
            
            # For text-based summary, we still need the raw text
            import pypdf
            reader = pypdf.PdfReader(BytesIO(file_bytes))
            raw_text = "".join(page.extract_text() or "" for page in reader.pages)

        else:
            return {"error": "This model currently only supports PDF files."}
    except Exception as e:
        print(f"Error converting PDF to image: {e}")
        return {"error": "Could not process PDF file."}

    # Ask questions to the document
    name = extract_from_document(first_page_image, "What is the full name of the applicant?")
    email = extract_from_document(first_page_image, "What is the email address?")
    phone = extract_from_document(first_page_image, "What is the phone number?")
    education = extract_from_document(first_page_image, "What is the university or college name mentioned in education?")
    
    # For skills, we fall back to our regex on the raw text for now
    SKILLS = ["React", "TypeScript", "Node.js", "Python", "AWS", "Docker", "GraphQL", "MongoDB", "JavaScript", "HTML", "CSS", "SQL", "Java", "C++", "Go", "Kubernetes"]
    skills_list = {skill for skill in SKILLS if re.search(r"\b" + re.escape(skill) + r"\b", raw_text, re.IGNORECASE)}

    # Generate summary from the raw text
    summary = generate_summary(raw_text)

    return {
        "full_name": name,
        "email": email,
        "phone": phone,
        "location": "N/A (Model does not extract this well)",
        "current_title": "N/A (Model does not extract this well)",
        "experience": "N/A (Model does not extract this well)",
        "skills": list(skills_list),
        "education": education,
        "professional_summary": summary,
        "raw_text": raw_text[:2000]
    }

# The match score function is still useful
def calculate_match_score(candidate_skills: List[str], job_skills: List[str]) -> int:
    # ... (this function is unchanged)
    if not job_skills: return 0
    candidate_skills = candidate_skills or []
    common_skills = set(c.lower() for c in candidate_skills) & set(j.lower() for j in job_skills)
    return int((len(common_skills) / len(job_skills)) * 100)