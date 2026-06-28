from recruitment.models import CandidateProfile, JobProfile


def calculate_ai_score(application):

    candidate_profile = CandidateProfile.objects.get(
        candidate=application.candidate
    )

    job_profile = JobProfile.objects.get(
        job=application.job
    )

    candidate_skills = set(
        skill.lower()
        for skill in candidate_profile.extracted_data.get("skills", [])
    )

    job_skills = set(
        skill.lower()
        for skill in job_profile.extracted_data.get("skills", [])
    )

    if not job_skills:
        return 0

    matched_skills = candidate_skills.intersection(job_skills)

    score = (len(matched_skills) / len(job_skills)) * 100

    return round(score, 2)