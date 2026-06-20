def calculate_score(job_skills, candidate_skills):

    job_skills = [
        skill.strip().lower()
        for skill in job_skills.split(",")
    ]

    candidate_skills = [
        skill.strip().lower()
        for skill in candidate_skills
    ]

    matched = [
        skill
        for skill in job_skills
        if skill in candidate_skills
    ]

    if not job_skills:
        return 0

    score = (len(matched) / len(job_skills)) * 100

    return round(score, 2)