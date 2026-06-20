import google.generativeai as genai
from django.conf import settings
import json

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def extract_resume_data(resume_text):

    prompt = f"""
    Extract the following information from the resume.

    Return ONLY valid JSON.

    {{
        "name": "",
        "skills": [],
        "projects": [],
        "education": [],
        "experience": []
    }}

    Resume:
    {resume_text}
    """

    response = model.generate_content(prompt)

    cleaned = response.text.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    return json.loads(cleaned)


import json

def extract_job_data(job_description):

    prompt = f"""
    Extract only technical skills from this job description.

    Return ONLY JSON.

    Format:

    {{
        "skills": []
    }}

    Job Description:
    {job_description}
    """

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)



def generate_interview_questions(
    candidate_skills,
    job_skills
):

    prompt = f"""
    Generate 10 technical interview questions.

    Candidate Skills:
    {candidate_skills}

    Job Skills:
    {job_skills}

    Return JSON only.

    {{
        "questions": [
            "question1",
            "question2"
        ]
    }}
    """

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)
