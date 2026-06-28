from django.db import models

class Job(models.Model):
    PROCESSING_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField()
    experience = models.IntegerField()

    ai_data = models.JSONField(
        null=True,
        blank=True
    )

    processing_status = models.CharField(
        max_length=20,
        choices=PROCESSING_CHOICES,
        default="PENDING"
    )

    processing_started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    processing_completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    processing_error = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Candidate(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    resume = models.FileField(
        upload_to="resumes/",
        null=True,
        blank=True,
    )

    processing_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    ) 
    processing_started_at = models.DateTimeField(null=True,blank=True,)

    processing_completed_at = models.DateTimeField(null=True,blank=True,)
    processing_error = models.TextField(blank=True,default="",)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
     

class Application(models.Model):
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    ai_score = models.FloatField(null=True,blank=True)


class CandidateProfile(models.Model):

    candidate = models.OneToOneField(Candidate,on_delete=models.CASCADE)
    extracted_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate.name

class JobProfile(models.Model):

    job = models.OneToOneField(Job,on_delete=models.CASCADE)
    extracted_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job.title      