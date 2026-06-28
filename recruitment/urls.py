from django.urls import path
from .views import (JobListAPIView, JobCreateAPIView, JobDetailAPIView, JobUpdateAPIView, JobDeleteAPIView, CandidateListAPIView, CandidateCreateAPIView, CandidateDetailAPIView, CandidateUpdateAPIView, CandidateDeleteAPIView, ApplicationListAPIView, ApplicationCreateAPIView, ApplicationDetailAPIView, ApplicationUpdateAPIView, ApplicationDeleteAPIView, ProcessJobAPIView, ProcessResumeAPIView ,RankCandidatesAPIView, GenerateInterviewQuestionsAPIView, SkillGapAnalysisAPIView, RecommendationAPIView, CandidateStatusAPIView, StartJobRankingAPIView)

urlpatterns = [
    path("jobs/" ,JobListAPIView.as_view(),  name="job-list"),
    path("jobs/create/", JobCreateAPIView.as_view(), name="job-create"), 
    path("jobs/<int:pk>/", JobDetailAPIView.as_view(), name="job-detail"),
    path("jobs/<int:pk>/update/",JobUpdateAPIView.as_view(), name="job-update"),
    path("jobs/<int:pk>/delete/", JobDeleteAPIView.as_view(), name="job-delete"),
    path("candidates/",CandidateListAPIView.as_view(),name="candidate-list"),
    path("candidates/create/",CandidateCreateAPIView.as_view(),name="candidate-create"),
    path("candidates/<int:pk>/",CandidateDetailAPIView.as_view(),name="candidate-detail"),
    path("candidates/<int:pk>/update/",CandidateUpdateAPIView.as_view(),name="candidate-update"),
    path("candidates/<int:pk>/delete/", CandidateDeleteAPIView.as_view(),name="candidate-delete"),
    path("applications/",ApplicationListAPIView.as_view(),name="application-list"),
    path("applications/create/",ApplicationCreateAPIView.as_view(),name="application-create"),
    path("applications/<int:pk>/",ApplicationDetailAPIView.as_view(),name="application-detail"),
    path("applications/<int:pk>/update/",ApplicationUpdateAPIView.as_view(),name="application-update"),
    path("applications/<int:pk>/delete/",ApplicationDeleteAPIView.as_view(),name="application-delete"),
    path("candidates/<int:pk>/process-resume/",ProcessResumeAPIView.as_view(),name="process-resume"),
    path("jobs/<int:pk>/process-job/",ProcessJobAPIView.as_view(),name="process-job"),
    path("jobs/<int:pk>/rank-candidates/",RankCandidatesAPIView.as_view(),name="rank-candidates"),
    path("applications/<int:pk>/generate-questions/",GenerateInterviewQuestionsAPIView.as_view(),name="generate-questions"),
    path("applications/<int:pk>/skill-gap/",SkillGapAnalysisAPIView.as_view(),name="skill-gap"),
    path("applications/<int:pk>/recommendation/",RecommendationAPIView.as_view(),name="recommendation"),
    path("candidates/<int:pk>/status/",CandidateStatusAPIView.as_view(),),
    path("jobs/<int:pk>/start-ranking/",StartJobRankingAPIView.as_view(),),
]    
