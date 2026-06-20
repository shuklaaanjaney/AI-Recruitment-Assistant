from rest_framework import generics , status
from .models import Job , Candidate , Application , CandidateProfile, JobProfile
from .serializers import JobSerializer , CandidateSerializer, ApplicationSerializer
from rest_framework.response import Response
from recruitment.services.resume_processor import process_resume
from rest_framework.views import APIView
from recruitment.services.job_processor import process_job
from .services.interview_generator import (generate_questions)

class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobCreateAPIView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobDetailAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer    

class JobUpdateAPIView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer    


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
            extracted_data = process_resume(candidate)

            profile, created = CandidateProfile.objects.update_or_create(
                candidate=candidate,
                defaults={
                    "extracted_data": extracted_data
                }
            )

            return Response(
                {
                    "message": "Resume processed successfully",
                    "candidate_id": candidate.id,
                    "data": extracted_data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )         

class ProcessJobAPIView(APIView):

    def post(self, request, pk):

        job = Job.objects.get(pk=pk)

        extracted_data = process_job(job)

        JobProfile.objects.update_or_create(
            job=job,
            defaults={
                "extracted_data": extracted_data
            }
        )

        return Response(extracted_data)   



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


class GenerateInterviewQuestionsAPIView(
    APIView
):

    def post(self, request, pk):

        try:

            application = Application.objects.get(
                pk=pk
            )

            candidate_profile = (
                CandidateProfile.objects.get(
                    candidate=application.candidate
                )
            )

            job_profile = (
                JobProfile.objects.get(
                    job=application.job
                )
            )

            questions = generate_questions(
                candidate_profile,
                job_profile
            )

            return Response({
                "candidate":
                application.candidate.name,

                "job":
                application.job.title,

                "ai_score":
                application.ai_score,

                "questions":
                questions["questions"]
            })

        except Application.DoesNotExist:

            return Response(
                {
                    "error":
                    "Application not found"
                },
                status=404
            )


class SkillGapAnalysisAPIView(APIView):

    def get(self, request, pk):

        try:

            application = Application.objects.get(pk=pk)

            candidate_profile = CandidateProfile.objects.get(
                candidate=application.candidate
            )

            job_profile = JobProfile.objects.get(
                job=application.job
            )

            candidate_skills = [
                skill.strip().lower()
                for skill in candidate_profile.extracted_data.get(
                    "skills",
                    []
                )
            ]

            job_skills = [
                skill.strip().lower()
                for skill in job_profile.extracted_data.get(
                    "skills",
                    []
                )
            ]

            matched_skills = [
                skill
                for skill in job_skills
                if skill in candidate_skills
            ]

            missing_skills = [
                skill
                for skill in job_skills
                if skill not in candidate_skills
            ]

            return Response({
                "candidate": application.candidate.name,
                "job": application.job.title,
                "ai_score": application.ai_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills
            })

        except Application.DoesNotExist:

            return Response(
                {
                    "error": "Application not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

class RecommendationAPIView(APIView):

    def get(self, request, pk):

        try:

            application = Application.objects.get(
                pk=pk
            )

            score = application.ai_score or 0

            if score >= 80:
                recommendation = (
                    "Strongly Recommend"
                )

                reason = (
                    "Candidate is an excellent match for the job."
                )

            elif score >= 60:
                recommendation = (
                    "Shortlist for Interview"
                )

                reason = (
                    "Candidate meets most of the required skills."
                )

            elif score >= 40:
                recommendation = (
                    "Consider"
                )

                reason = (
                    "Candidate partially matches the job requirements."
                )

            else:
                recommendation = (
                    "Not Recommended"
                )

                reason = (
                    "Candidate does not match enough required skills."
                )

            return Response({
                "candidate":
                application.candidate.name,

                "job":
                application.job.title,

                "ai_score":
                score,

                "recommendation":
                recommendation,

                "reason":
                reason
            })

        except Application.DoesNotExist:

            return Response(
                {
                    "error":
                    "Application not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class DashboardAPIView(APIView):

    def get(self, request):

        top_application = (
            Application.objects
            .filter(ai_score__isnull=False)
            .order_by("-ai_score")
            .first()
        )

        return Response({

            "total_jobs":
            Job.objects.count(),

            "total_candidates":
            Candidate.objects.count(),

            "total_applications":
            Application.objects.count(),

            "processed_resumes":
            CandidateProfile.objects.count(),

            "processed_jobs":
            JobProfile.objects.count(),

            "top_candidate":
            {
                "name":
                top_application.candidate.name
                if top_application else None,

                "score":
                top_application.ai_score
                if top_application else None
            }
        })


