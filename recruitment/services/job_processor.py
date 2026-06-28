from recruitment.ai_utils import extract_job_data


def process_job(job):

    job_text = f"""
    Job Title:
    {job.title}

    Description:
    {job.description}

    Required Skills:
    {job.required_skills}

    Experience:
    {job.experience} years
    """

    extracted_data = extract_job_data(job_text)

    return extracted_data