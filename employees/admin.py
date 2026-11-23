from django.contrib import admin
from .models import (
    Candidate,
    Job,
    Application,
    AIInterview,
    AIInterviewQuestion
)


# =========================
# CANDIDATE ADMIN
# =========================

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'education'
    )


# =========================
# JOB ADMIN
# =========================

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'company',
        'location',
        'experience',
        'salary',
        'created_at'
    )

    search_fields = (
        'title',
        'company',
        'location'
    )


# =========================
# APPLICATION ADMIN
# =========================

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'candidate',
        'job',
        'status',
        'interview_status',
        'interview_date',
        'interview_time',
        'applied_at'
    )

    list_filter = (
        'status',
        'interview_status'
    )

    search_fields = (
        'candidate__user__username',
        'job__title',
        'job__company'
    )


# =========================
# AI INTERVIEW ADMIN
# =========================

@admin.register(AIInterview)
class AIInterviewAdmin(admin.ModelAdmin):
    list_display = (
        'application',
        'completed',
        'total_score',
        'started_at'
    )

    list_filter = (
        'completed',
    )


# =========================
# AI INTERVIEW QUESTION ADMIN
# =========================

@admin.register(AIInterviewQuestion)
class AIInterviewQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'interview',
        'question',
        'score'
    )