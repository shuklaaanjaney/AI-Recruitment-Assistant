from rest_framework import serializers
from .models import Job , Candidate , Application


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = "__all__"


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = "__all__"        



class ApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(
        source='candidate.name',
        read_only=True
    )

    job_title = serializers.CharField(
        source='job.title',
        read_only=True
    )

    class Meta:
        model = Application
        fields = "__all__"
