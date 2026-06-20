from recruitment.ai_utils import (
    generate_interview_questions
)


def generate_questions(
    candidate_profile,
    job_profile
):

    candidate_skills = (
        candidate_profile.extracted_data.get(
            "skills",
            []
        )
    )

    job_skills = (
        job_profile.extracted_data.get(
            "skills",
            []
        )
    )

    return generate_interview_questions(
        candidate_skills,
        job_skills
    )