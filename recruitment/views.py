from rest_framework import generics , status
from .models import Job , Candidate , Application , CandidateProfile, JobProfile
from .serializers import JobSerializer , CandidateSerializer, ApplicationSerializer
from rest_framework.response import Response
from recruitment.tasks import process_resume_task
from rest_framework.views import APIView
from recruitment.services.job_processor import process_job
from .services.interview_generator import (generate_questions)
from django.core.cache import cache
from recruitment.tasks import process_job_task
from recruitment.tasks import rank_candidate_task
from recruitment.services.skill_gap_service import analyze_skill_gap
from recruitment.services.recommendation_service import generate_recommendation
from .serializers import (
    ProcessResumeResponseSerializer,
    CandidateStatusResponseSerializer,
    ProcessJobResponseSerializer,
    RankingResponseSerializer,
    SkillGapResponseSerializer,
    RecommendationResponseSerializer,
    InterviewQuestionsResponseSerializer,)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)

@extend_schema(
    tags=["Jobs"],
    summary="List Jobs",
    description="Returns all available jobs."
)

class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

@extend_schema(
    tags=["Jobs"],
    summary="Create Job",
    description="Create a new job posting.",
    request=JobSerializer,
    responses={
        201: JobSerializer
    }
)
class JobCreateAPIView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

@extend_schema(
    tags=["Jobs"],
    summary="Get Job",
    description="Retrieve a job by its ID.",
    responses={
        200: JobSerializer,
        404: OpenApiResponse(description="Job not found")
    }
)
class JobDetailAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer  

@extend_schema(
    tags=["Jobs"],
    summary="Update Job",
    request=JobSerializer,
    responses={
        200: JobSerializer
    }
)
class JobUpdateAPIView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer    

@extend_schema(
    tags=["Jobs"],
    summary="Delete Job",
    responses={
        204: OpenApiResponse(description="Job deleted")
    }
)

class JobDeleteAPIView(generics.DestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        job_title = instance.title

        instance.delete()

        return Response(
            {
                "message": f"Job '{job_title}' deleted successfully"
            },
            status=status.HTTP_200_OK
        )


class CandidateListAPIView(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateCreateAPIView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateDetailAPIView(generics.RetrieveAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer    

class CandidateUpdateAPIView(generics.UpdateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer    


class CandidateDeleteAPIView(generics.DestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        candidate_name = instance.name
        self.perform_destroy(instance)

        return Response(
           {
            "message": f"Candidate '{candidate_name}' deleted successfully"
        },
        status=status.HTTP_200_OK
    )        


class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer   


class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def perform_create(self, serializer):

        application = serializer.save()

        try:

            profile = CandidateProfile.objects.get(
                candidate=application.candidate
            )

            job_profile = JobProfile.objects.get(
                job=application.job
            )

            candidate_skills = profile.extracted_data.get(
                "skills",
                []
            )

            job_skills = job_profile.extracted_data.get(
                "skills",
                []
            )

            candidate_skills = [
                skill.strip().lower()
                for skill in candidate_skills
            ]

            job_skills = [
                skill.strip().lower()
                for skill in job_skills
            ]

            matched_skills = [
                skill
                for skill in job_skills
                if skill in candidate_skills
            ]

            if len(job_skills) > 0:
                score = (
                    len(matched_skills)
                    / len(job_skills)
                ) * 100
            else:
                score = 0

            print("Candidate Skills:", candidate_skills)
            print("Job Skills:", job_skills)
            print("Matched Skills:", matched_skills)
            print("Score:", score)    

            application.ai_score = round(score, 2)
            application.save()

        except (
            CandidateProfile.DoesNotExist,
            JobProfile.DoesNotExist
        ):
            application.ai_score = 0
            application.save()

class ApplicationDetailAPIView(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer    


class ApplicationUpdateAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer    

class ApplicationDeleteAPIView(generics.DestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        candidate_name = instance.candidate.name

        job_title = instance.job.title

        self.perform_destroy(instance)

        return Response(
            {
                "message":
                f"Application of '{candidate_name}' for '{job_title}' deleted successfully"
            },
            status=status.HTTP_200_OK
        )

@extend_schema(
    tags=["AI Processing"],
    summary="Process Resume",
    description="""
Extract candidate information from a resume using Gemini AI.
The task is executed asynchronously using Celery.
""",
    responses={
        202: ProcessResumeResponseSerializer
    }
)

class ProcessResumeAPIView(APIView):

    def post(self, request, pk):

        try:
            candidate = Candidate.objects.get(pk=pk)

        except Candidate.DoesNotExist:
            return Response(
                {
                    "error": "Candidate not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        
        if not candidate.resume:
            return Response(
                {
                    "error": "No resume uploaded for this candidate"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            candidate.processing_status = "PENDING"
            candidate.processing_started_at = None
            candidate.processing_completed_at = None
            candidate.processing_error = ""
            candidate.save()

            process_resume_task.delay(candidate.id)

            return Response(
        {
            "message": "Resume uploaded.",
            "status": "Processing started.",
            "candidate_id": candidate.id,
        },
        status=status.HTTP_202_ACCEPTED,
    )

        except Exception as e:

            return Response(
        {
            "error": str(e)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )       
@extend_schema(
    tags=["AI Processing"],
    summary="Process Job Description",
    description="""
Uses Gemini AI to extract skills from a job description.
The task runs asynchronously using Celery.
""",
    parameters=[
        OpenApiParameter(
            name="pk",
            type=int,
            location=OpenApiParameter.PATH,
            description="Job ID"
        )
    ],
    responses={
        202: ProcessJobResponseSerializer,
        404: OpenApiResponse(description="Job not found")
    }
)
class ProcessJobAPIView(APIView):

    def post(self, request, pk):

        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        process_job_task.delay(job.id)

        return Response(
            {
                "message": "Job processing started.",
                "status": "PROCESSING",
                "job_id": job.id,
            },
            status=status.HTTP_202_ACCEPTED,
        )


@extend_schema(
    tags=["AI Matching"],
    summary="Rank Candidates",
    description="""
Returns all candidates ranked according to AI score.
""",
    responses={
        200: RankingResponseSerializer
    }
)
class RankCandidatesAPIView(APIView):

    def get(self, request, pk):

        try:
            job = Job.objects.get(pk=pk)

        except Job.DoesNotExist:
            return Response(
                {
                    "error": "Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        applications = (
            Application.objects
            .filter(
                job=job,
                ai_score__isnull=False
            )
            .order_by("-ai_score")
        )

        ranked_candidates = []

        for rank, application in enumerate(
            applications,
            start=1
        ):

            ranked_candidates.append(
                {
                    "rank": rank,
                    "candidate_id": application.candidate.id,
                    "candidate_name": application.candidate.name,
                    "ai_score": application.ai_score,
                    "application_status": application.status
                }
            )

        return Response(
            {
                "job_id": job.id,
                "job_title": job.title,
                "total_candidates": len(ranked_candidates),
                "rankings": ranked_candidates
            },
            status=status.HTTP_200_OK
        )


@extend_schema(
    summary="Generate AI Interview Questions",
    description="""
Generate interview questions using the candidate's processed
resume and the processed job description.
""",
    parameters=[
        OpenApiParameter(
            name="pk",
            type=int,
            location=OpenApiParameter.PATH,
            description="Application ID"
        )
    ],
    responses={
        200: InterviewQuestionsResponseSerializer
    }
)
class GenerateInterviewQuestionsAPIView(APIView):

    def get(self, request, pk):

        try:

            application = Application.objects.get(pk=pk)

        except Application.DoesNotExist:

            return Response(
                {
                    "error": "Application not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            candidate_profile = CandidateProfile.objects.get(
                candidate=application.candidate
            )

            job_profile = JobProfile.objects.get(
                job=application.job
            )

        except (
            CandidateProfile.DoesNotExist,
            JobProfile.DoesNotExist
        ):

            return Response(
                {
                    "error": "Resume or Job not processed yet."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        questions = generate_questions(
            candidate_profile,
            job_profile
        )

        return Response({

            "candidate": application.candidate.name,

            "job": application.job.title,

            "questions": questions["questions"]

        })


@extend_schema(
    summary="Skill Gap Analysis",
    description="Compare candidate skills with required job skills.",
    responses={
        200: SkillGapResponseSerializer
    }
)

class SkillGapAnalysisAPIView(APIView):

    def get(self, request, pk):

        try:
            application = Application.objects.get(pk=pk)

        except Application.DoesNotExist:
            return Response(
                {
                    "error": "Application not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            candidate_profile = CandidateProfile.objects.get(
                candidate=application.candidate
            )

            job_profile = JobProfile.objects.get(
                job=application.job
            )

        except (CandidateProfile.DoesNotExist, JobProfile.DoesNotExist):
            return Response(
                {
                    "error": "Candidate or Job has not been processed yet."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = analyze_skill_gap(
            candidate_profile,
            job_profile
        )

        return Response(
            {
                "candidate": application.candidate.name,
                "job": application.job.title,
                "ai_score": application.ai_score,
                **result
            },
            status=status.HTTP_200_OK
        )


@extend_schema(
    summary="AI Recommendation",
    description="Returns an AI recommendation based on score and skill gap.",
    responses={
        200: RecommendationResponseSerializer
    }
)

class RecommendationAPIView(APIView):

    def get(self, request, pk):

        try:
            application = Application.objects.get(pk=pk)

        except Application.DoesNotExist:
            return Response(
                {
                    "error": "Application not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            candidate_profile = CandidateProfile.objects.get(
                candidate=application.candidate
            )

            job_profile = JobProfile.objects.get(
                job=application.job
            )

        except (CandidateProfile.DoesNotExist,
                JobProfile.DoesNotExist):

            return Response(
                {
                    "error": "Candidate or Job has not been processed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        skill_gap = analyze_skill_gap(
            candidate_profile,
            job_profile
        )

        recommendation = generate_recommendation(
            application.ai_score or 0,
            skill_gap["matched_skills"],
            skill_gap["missing_skills"]
        )

        return Response({

            "candidate": application.candidate.name,

            "job": application.job.title,

            "ai_score": application.ai_score,

            "match_percentage": skill_gap["match_percentage"],

            "matched_skills": skill_gap["matched_skills"],

            "missing_skills": skill_gap["missing_skills"],

            **recommendation

        })


class DashboardAPIView(APIView):

    def get(self, request):

        dashboard_data = cache.get("dashboard_data")

        if dashboard_data:

            print("Dashboard loaded from Redis Cache")

            return Response(dashboard_data)

        print("Dashboard loaded from PostgreSQL")

        top_application = (
            Application.objects
            .filter(ai_score__isnull=False)
            .order_by("-ai_score")
            .first()
        )

        dashboard_data = {

            "total_jobs": Job.objects.count(),

            "total_candidates": Candidate.objects.count(),

            "total_applications": Application.objects.count(),

            "processed_resumes": CandidateProfile.objects.count(),

            "processed_jobs": JobProfile.objects.count(),

            "top_candidate": {

                "name": top_application.candidate.name
                if top_application else None,

                "score": top_application.ai_score
                if top_application else None
            }
        }
        cache.set("dashboard_data", dashboard_data, timeout=300)

        return Response(dashboard_data)

@extend_schema(
    tags=["AI Processing"],
    summary="Resume Processing Status",
    description="Returns the current status of resume processing.",
    responses={
        200: CandidateStatusResponseSerializer
    }
)
class CandidateStatusAPIView(APIView):

    def get(self, request, pk):

        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response(
                {"error": "Candidate not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({
            "candidate": candidate.name,
            "status": candidate.processing_status,
            "started_at": candidate.processing_started_at,
            "completed_at": candidate.processing_completed_at,
            "error": candidate.processing_error,
        })        



class StartJobRankingAPIView(APIView):

    def post(self, request, pk):

        try:
            job = Job.objects.get(pk=pk)

        except Job.DoesNotExist:

            return Response(
                {
                    "error": "Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        applications = Application.objects.filter(job=job)

        if not applications.exists():

            return Response(
                {
                    "error": "No applications found for this job"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        for application in applications:

            rank_candidate_task.delay(application.id)

        return Response(
            {
                "message": "Ranking started successfully.",
                "job": job.title,
                "applications": applications.count()
            },
            status=status.HTTP_202_ACCEPTED
        )


