def generate_recommendation(
    ai_score,
    matched_skills,
    missing_skills
):

    if ai_score >= 85:
        return {
            "recommendation": "Strongly Recommend",
            "decision": "SHORTLIST",
            "reason": (
                "Excellent skill match. Candidate is ready for interview."
            )
        }

    elif ai_score >= 70:
        return {
            "recommendation": "Recommend with Training",
            "decision": "CONSIDER",
            "reason": (
                f"Candidate is missing {len(missing_skills)} required skill(s): "
                + ", ".join(missing_skills)
            )
        }

    else:
        return {
            "recommendation": "Not Recommended",
            "decision": "REJECT",
            "reason": (
                "Skill match is too low for this role."
            )
        }