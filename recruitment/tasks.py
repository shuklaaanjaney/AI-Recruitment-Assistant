from celery import shared_task
from django.utils import timezone
from recruitment.services.resume_processor import process_resume
from django.core.cache import cache
from recruitment.services.job_processor import process_job
from recruitment.models import (Candidate,CandidateProfile,Job,JobProfile,)
from recruitment.models import Application
from recruitment.services.ranking_service import calculate_ai_score

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_resume_task(candidate_id):

    candidate = Candidate.objects.get(id=candidate_id)

    candidate.processing_status = "PROCESSING"
    candidate.processing_started_at = timezone.now()
    candidate.processing_error = ""
    candidate.save()

    try:

        extracted_data = process_resume(candidate)

        CandidateProfile.objects.update_or_create(
            candidate=candidate,
            defaults={
                "extracted_data": extracted_data
            }
        )

        candidate.processing_status = "COMPLETED"
        candidate.processing_completed_at = timezone.now()
        candidate.save()

        cache.delete("dashboard_context")

        return "Resume processed successfully"

    except Exception as e:

        candidate.processing_status = "FAILED"
        candidate.processing_completed_at = timezone.now()
        candidate.processing_error = str(e)
        candidate.save()

        raise


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_job_task(job_id):

    print("========== JOB TASK STARTED ==========")

    job = Job.objects.get(id=job_id)

    print("Job:", job.title)

    job.processing_status = "PROCESSING"
    job.processing_started_at = timezone.now()
    job.processing_error = ""
    job.save()

    try:

        extracted_data = process_job(job)

        print("Job processed")

        # Save AI data inside Job model
        job.ai_data = extracted_data

        # Save extracted data in JobProfile
        JobProfile.objects.update_or_create(
            job=job,
            defaults={
                "extracted_data": extracted_data
            }
        )

        print("JobProfile saved")

        job.processing_status = "COMPLETED"
        job.processing_completed_at = timezone.now()
        job.save()

        cache.delete("dashboard_context")

        print("Dashboard cache cleared")
        print("Job processed successfully.")

        return "Job processed successfully"

    except Exception as e:

        print("Job Failed:", str(e))

        job.processing_status = "FAILED"
        job.processing_completed_at = timezone.now()
        job.processing_error = str(e)
        job.save()

        raise

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def rank_candidate_task(application_id):

    print("========== RANKING TASK STARTED ==========")

    application = Application.objects.get(id=application_id)

    print("Candidate:", application.candidate.name)
    print("Job:", application.job.title)

    try:

        score = calculate_ai_score(application)

        application.ai_score = score
        application.save()

        cache.delete("dashboard_context")

        print("AI Score:", score)
        print("Dashboard cache cleared")
        print("Ranking completed successfully")

        return score

    except Exception as e:

        print("Ranking Failed:", str(e))
        raise
