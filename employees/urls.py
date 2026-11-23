from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # Home Page
    path('', views.home, name='home'),

    # Candidate Registration
    path('register/', views.register, name='register'),

    # Candidate Login
    path('login/', views.user_login, name='login'),

    # Candidate Dashboard
    path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),

    # Logout
    path('logout/', views.user_logout, name='logout'),

    # Available Jobs
    path('jobs/', views.available_jobs, name='available_jobs'),

    # Job Details
    path('jobs/<int:job_id>/', views.job_details, name='job_details'),

    # Apply for Job
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),

    # Application Status
    path('applications/', views.application_status, name='application_status'),

    # HR Dashboard
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),

    # HR Candidates
    path(
        'hr-dashboard/candidates/',
        views.hr_candidates,
        name='hr_candidates'
    ),

    # HR Applications
    path(
        'hr-dashboard/applications/',
        views.hr_applications,
        name='hr_applications'
    ),

    # Shortlisted Applications
    path(
        'hr-dashboard/shortlisted/',
        views.shortlisted_applications,
        name='hr_shortlisted'
    ),

    # Add Job
    path(
        'hr-dashboard/add-job/',
        views.add_job,
        name='add_job'
    ),

    # Manage Jobs
    path(
        'hr-dashboard/manage-jobs/',
        views.manage_jobs,
        name='manage_jobs'
    ),

    # Edit Job
    path(
        'hr-dashboard/edit-job/<int:job_id>/',
        views.edit_job,
        name='edit_job'
    ),

    # Delete Job
    path(
        'hr-dashboard/delete-job/<int:job_id>/',
        views.delete_job,
        name='delete_job'
    ),

    # Update Application Status
    path(
        'hr-dashboard/application/<int:application_id>/update/',
        views.update_application_status,
        name='update_application_status'
    ),

    # Candidate Profile
    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    # Forgot Password
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='employees/password_reset.html'
        ),
        name='password_reset'
    ),

    # Password Reset Email Sent
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='employees/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # New Password
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='employees/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # Password Reset Complete
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='employees/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    # AI Job Match
    path(
    'jobs/<int:job_id>/ai-match/',
    views.ai_job_match,
    name='ai_job_match'
),
# Start AI Interview
path(
    'ai-interview/<int:interview_id>/',
    views.ai_interview,
    name='ai_interview'
),

# AI Interview Result
path(
    'ai-interview/<int:interview_id>/result/',
    views.ai_interview_result,
    name='ai_interview_result'
),
# Schedule Interview
path(
    'hr-dashboard/application/<int:application_id>/schedule-interview/',
    views.schedule_interview,
    name='schedule_interview'
),
# AI Job Matching
path(
    'jobs/<int:job_id>/ai-match/',
    views.ai_job_match,
    name='ai_job_match'
),

# Start AI Interview
path(
    'ai-interview/start/<int:application_id>/',
    views.start_ai_interview,
    name='start_ai_interview'
),

# AI Interview
path(
    'ai-interview/<int:interview_id>/',
    views.ai_interview,
    name='ai_interview'
),

# AI Interview Result
path(
    'ai-interview/<int:interview_id>/result/',
    views.ai_interview_result,
    name='ai_interview_result'
),

# Notifications
path(
    'notifications/',
    views.candidate_notifications,
    name='candidate_notifications'
),

path(
    'notifications/read/<int:notification_id>/',
    views.mark_notification_read,
    name='mark_notification_read'
),
]