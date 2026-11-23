from django.db import models
from django.contrib.auth.models import User


# =========================
# CANDIDATE MODEL
# =========================

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    education = models.CharField(max_length=200)
    skills = models.TextField()
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


# =========================
# JOB MODEL
# =========================

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    experience = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# APPLICATION MODEL
# =========================

class Application(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    # =========================
    # INTERVIEW DETAILS
    # =========================

    INTERVIEW_STATUS_CHOICES = [
        ('Not Scheduled', 'Not Scheduled'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    interview_date = models.DateField(
        blank=True,
        null=True
    )

    interview_time = models.TimeField(
        blank=True,
        null=True
    )

    interview_mode = models.CharField(
        max_length=50,
        blank=True
    )

    interview_status = models.CharField(
        max_length=20,
        choices=INTERVIEW_STATUS_CHOICES,
        default='Not Scheduled'
    )

    def __str__(self):
        return f"{self.candidate} - {self.job}"

    # =========================
    # AI INTERVIEW MODEL
    # =========================

class AIInterview(models.Model):
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    completed = models.BooleanField(
        default=False
    )

    total_score = models.IntegerField(
        default=0
    )

    def __str__(self):
        return f"AI Interview - {self.application.candidate.user.username}"


    # =========================
    # AI INTERVIEW QUESTION
    # =========================

class AIInterviewQuestion(models.Model):
    interview = models.ForeignKey(
        AIInterview,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question = models.TextField()

    answer = models.TextField(
        blank=True
    )

    score = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.question

    # =========================
# NOTIFICATION MODEL
# =========================

class Notification(models.Model):

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.user.username} - {self.message}"