from pypdf import PdfReader
from recruitment.ai_utils import extract_resume_data




def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def process_resume(candidate):
    pdf_path = candidate.resume.path
    resume_text = extract_text_from_pdf(pdf_path)
    extracted_data = extract_resume_data(resume_text)
    return extracted_data