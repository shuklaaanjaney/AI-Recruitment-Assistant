def analyze_skill_gap(candidate_profile, job_profile):

    candidate_skills = {
        skill.lower()
        for skill in candidate_profile.extracted_data.get("skills", [])
    }

    job_skills = {
        skill.lower()
        for skill in job_profile.extracted_data.get("skills", [])
    }

    matched_skills = sorted(
        candidate_skills.intersection(job_skills)
    )

    missing_skills = sorted(
        job_skills.difference(candidate_skills)
    )

    match_percentage = 0

    if job_skills:
        match_percentage = round(
            (len(matched_skills) / len(job_skills)) * 100,
            2
        )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }