from pypdf import PdfReader
import google.generativeai as genai
from django.conf import settings

genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)
import json

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text

def get_candidate_resume_text(candidate):
    return extract_text_from_pdf(
        candidate.resume.path
    )    




