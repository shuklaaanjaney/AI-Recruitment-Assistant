from recruitment.ai_utils import extract_job_data


def process_job(job):

    extracted_data = extract_job_data(
        job.required_skills
    )

    return extracted_data