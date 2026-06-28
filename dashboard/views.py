from django.shortcuts import render
from recruitment.models import (Job,Candidate,Application,CandidateProfile,JobProfile)
from recruitment.services.interview_generator import (generate_questions)
from django.core.cache import cache
from django.db.models import Avg

def dashboard_view(request):

    context = cache.get("dashboard_context")

    if context:
        print("Dashboard loaded from Redis Cache")
        return render(request, "dashboard/dashboard.html", context)

    print("Dashboard loaded from PostgreSQL")

    top_application = (
        Application.objects
        .filter(ai_score__isnull=False)
        .select_related("candidate")
        .order_by("-ai_score")
        .first()
    )

    top_candidates = (
        Application.objects
        .filter(ai_score__isnull=False)
        .select_related("candidate")
        .order_by("-ai_score")[:5]
    )

    average_score = (
        Application.objects
        .filter(ai_score__isnull=False)
        .aggregate(avg_score=Avg("ai_score"))
    )

    strong_recommendations = (
        Application.objects
        .filter(ai_score__gte=80)
        .count()
    )

    pending_resumes = (
        Candidate.objects
        .filter(processing_status="PENDING")
        .count()
    )

    completed_resumes = (
        Candidate.objects
        .filter(processing_status="COMPLETED")
        .count()
    )

    failed_resumes = (
        Candidate.objects
        .filter(processing_status="FAILED")
        .count()
    )

    pending_jobs = (
        Job.objects
        .filter(processing_status="PENDING")
        .count()
    )

    completed_jobs = (
        Job.objects
        .filter(processing_status="COMPLETED")
        .count()
    )

    context = {

        "total_jobs": Job.objects.count(),

        "total_candidates": Candidate.objects.count(),

        "total_applications": Application.objects.count(),

        "processed_resumes": CandidateProfile.objects.count(),

        "processed_jobs": JobProfile.objects.count(),

        "top_candidate": top_application,

        "top_candidates": top_candidates,

        "average_score": round(
            average_score["avg_score"] or 0,
            2
        ),

        "strong_recommendations": strong_recommendations,

        "pending_resumes": pending_resumes,

        "completed_resumes": completed_resumes,

        "failed_resumes": failed_resumes,

        "pending_jobs": pending_jobs,

        "completed_jobs": completed_jobs,
    }

    cache.set(
        "dashboard_context",
        context,
        timeout=300
    )

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


def interview_questions_page(
    request,
    pk
):

    application = Application.objects.get(
        pk=pk
    )

    questions = generate_questions(
        CandidateProfile.objects.get(
            candidate=application.candidate
        ),
        JobProfile.objects.get(
            job=application.job
        )
    )

    return render(
        request,
        "dashboard/questions.html",
        {
            "questions":
            questions["questions"]
        }
    )    
def candidate_list(request):

    candidates = Candidate.objects.all()

    return render(
        request,
        "dashboard/candidates.html",
        {
            "candidates": candidates
        }
    )


def job_list(request):

    jobs = Job.objects.all()

    return render(
        request,
        "dashboard/jobs.html",
        {
            "jobs": jobs
        }
    )


def ranking_page(request, pk):

    job = Job.objects.get(pk=pk)

    applications = (
        Application.objects
        .filter(
            job=job,
            ai_score__isnull=False
        )
        .order_by("-ai_score")
    )

    return render(
        request,
        "dashboard/ranking.html",
        {
            "job": job,
            "applications": applications
        }
    )


def skill_gap_page(request, pk):

    application = Application.objects.get(pk=pk)

    candidate_profile = CandidateProfile.objects.get(
        candidate=application.candidate
    )

    job_profile = JobProfile.objects.get(
        job=application.job
    )

    candidate_skills = candidate_profile.extracted_data.get(
        "skills",
        []
    )

    job_skills = job_profile.extracted_data.get(
        "skills",
        []
    )

    matched = [
        skill
        for skill in job_skills
        if skill in candidate_skills
    ]

    missing = [
        skill
        for skill in job_skills
        if skill not in candidate_skills
    ]

    return render(
        request,
        "dashboard/skill_gap.html",
        {
            "application": application,
            "matched": matched,
            "missing": missing
        }
    )