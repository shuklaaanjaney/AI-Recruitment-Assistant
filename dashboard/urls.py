from django.urls import path
from .views import dashboard_view, candidate_list, job_list, ranking_page, skill_gap_page, interview_questions_page

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("candidates/",candidate_list,name="candidate-list"),
    path("jobs/",job_list,name="job-list"),
    path("jobs/<int:pk>/ranking/",ranking_page,name="ranking-page"),
    path("applications/<int:pk>/skill-gap-page/",skill_gap_page, name="skill-gap-page"),
    path("applications/<int:pk>/questions/",interview_questions_page,name="questions-page"),
]