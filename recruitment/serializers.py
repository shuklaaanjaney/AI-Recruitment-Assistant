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


class ProcessResumeResponseSerializer(serializers.Serializer):

    message = serializers.CharField()
    status = serializers.CharField()
    candidate_id = serializers.IntegerField()


class CandidateStatusResponseSerializer(serializers.Serializer):

    candidate = serializers.CharField()
    status = serializers.CharField()
    started_at = serializers.DateTimeField(
        allow_null=True
    )
    completed_at = serializers.DateTimeField(
        allow_null=True
    )
    error = serializers.CharField()


class ProcessJobResponseSerializer(serializers.Serializer):

    message = serializers.CharField()
    status = serializers.CharField()
    job_id = serializers.IntegerField()


class RankingResponseSerializer(serializers.Serializer):

    rank = serializers.IntegerField()
    candidate_id = serializers.IntegerField()
    candidate_name = serializers.CharField()
    ai_score = serializers.FloatField()
    application_status = serializers.CharField()


class SkillGapResponseSerializer(serializers.Serializer):

    candidate = serializers.CharField()
    job = serializers.CharField()
    ai_score = serializers.FloatField()
    matched_skills = serializers.ListField(
        child=serializers.CharField()
    )
    missing_skills = serializers.ListField(
        child=serializers.CharField()
    )
    match_percentage = serializers.FloatField()


class RecommendationResponseSerializer(serializers.Serializer):

    candidate = serializers.CharField()
    job = serializers.CharField()
    ai_score = serializers.FloatField()
    match_percentage = serializers.FloatField()
    matched_skills = serializers.ListField(
        child=serializers.CharField()
    )
    missing_skills = serializers.ListField(
        child=serializers.CharField()
    )
    recommendation = serializers.CharField()
    decision = serializers.CharField()
    reason = serializers.CharField()


class InterviewQuestionsResponseSerializer(serializers.Serializer):

    candidate = serializers.CharField()
    job = serializers.CharField()
    questions = serializers.ListField(
        child=serializers.CharField()
    )