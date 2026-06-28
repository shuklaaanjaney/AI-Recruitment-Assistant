from django.contrib import admin
from .models import (
    Candidate,
    Job,
    Application,
    CandidateProfile,
    JobProfile,
)

admin.site.register(Candidate)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(CandidateProfile)
admin.site.register(JobProfile)