from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import ( Candidate,Job,Application,AIInterview,AIInterviewQuestion,Notification)
from .forms import CandidateRegistrationForm


# =========================
# HOME PAGE
# =========================

def home(request):
    return render(request, 'employees/home.html')


# =========================
# CANDIDATE REGISTRATION
# =========================

def register(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                return render(request, 'employees/register.html', {
                    'form': form,
                    'error': 'Username already exists. Please choose another username.'
                })

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            Candidate.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                education=form.cleaned_data['education'],
                skills=form.cleaned_data['skills'],
                resume=form.cleaned_data['resume']
            )

            return redirect('login')

    else:
        form = CandidateRegistrationForm()

    return render(request, 'employees/register.html', {
        'form': form
    })


# =========================
# LOGIN
# =========================

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            # HR/Admin login
            if user.is_staff:
                return redirect('hr_dashboard')

            # Candidate login
            return redirect('candidate_dashboard')

        return render(request, 'employees/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'employees/login.html')


# =========================
# CANDIDATE DASHBOARD
# =========================

def candidate_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    candidate, created = Candidate.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'education': '',
            'skills': ''
        }
    )

    applications = Application.objects.filter(
        candidate=candidate
    ).select_related('job').order_by('-applied_at')

    total_applications = applications.count()
    shortlisted = applications.filter(status='Shortlisted').count()
    selected = applications.filter(status='Selected').count()

    # Unread notifications count
    unread_notifications_count = Notification.objects.filter(
        candidate=candidate,
        is_read=False
    ).count()

    return render(request, 'employees/dashboard.html', {
        'candidate': candidate,
        'applications': applications[:3],
        'total_applications': total_applications,
        'shortlisted': shortlisted,
        'selected': selected,
        'unread_notifications_count': unread_notifications_count,
    })



# =========================
# LOGOUT
# =========================

def user_logout(request):
    logout(request)
    return redirect('login')


# =========================
# AVAILABLE JOBS
# =========================


def available_jobs(request):

    jobs = Job.objects.all().order_by('-created_at')

    # Search keyword
    search = request.GET.get('search', '').strip()

    # Search location
    location = request.GET.get('location', '').strip()

    # Search by job title, company or required skills
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(company__icontains=search) |
            Q(required_skills__icontains=search)
        )

    # Filter by location
    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    context = {
        'jobs': jobs,
        'search': search,
        'location': location,
    }

    return render(
        request,
        'employees/available_jobs.html',
        context
    )


# =========================
# JOB DETAILS
# =========================

def job_details(request, job_id):
    job = Job.objects.get(id=job_id)

    return render(request, 'employees/job_details.html', {
        'job': job
    })


# =========================
# AI JOB MATCH
# =========================

def ai_job_match(request, job_id):
    if not request.user.is_authenticated:
        return redirect('login')

    # HR/Admin should not use candidate AI matching page
    if request.user.is_staff:
        return redirect('hr_dashboard')

    candidate, created = Candidate.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'education': '',
            'skills': ''
        }
    )

    job = Job.objects.get(id=job_id)

    # Candidate skills
    candidate_skills = set(
        skill.strip().lower()
        for skill in candidate.skills.split(',')
        if skill.strip()
    )

    # Required job skills
    required_skills = set(
        skill.strip().lower()
        for skill in job.required_skills.split(',')
        if skill.strip()
    )

    # Matching skills
    matched_skills = candidate_skills.intersection(required_skills)

    # Missing skills
    missing_skills = required_skills - candidate_skills

    # Calculate match score
    if required_skills:
        match_score = round(
            (len(matched_skills) / len(required_skills)) * 100
        )
    else:
        match_score = 0

    return render(request, 'employees/ai_job_match.html', {
        'job': job,
        'match_score': match_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
    })


# =========================
# ADD JOB - HR
# =========================

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        return redirect('candidate_dashboard')

    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        description = request.POST.get('description')
        required_skills = request.POST.get('required_skills')
        experience = request.POST.get('experience')
        location = request.POST.get('location')
        salary = request.POST.get('salary')

        Job.objects.create(
            title=title,
            company=company,
            description=description,
            required_skills=required_skills,
            experience=int(experience) if experience else 0,
            location=location,
            salary=salary
        )

        return redirect('hr_dashboard')

    return render(request, 'employees/add_job.html')


# =========================
# APPLY FOR JOB
# =========================

def apply_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('login')

    candidate, created = Candidate.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'education': '',
            'skills': ''
        }
    )

    job = Job.objects.get(id=job_id)

    Application.objects.get_or_create(
        candidate=candidate,
        job=job
    )

    return redirect('application_status')


# =========================
# APPLICATION STATUS
# =========================

def application_status(request):
    if not request.user.is_authenticated:
        return redirect('login')

    candidate, created = Candidate.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'education': '',
            'skills': ''
        }
    )

    applications = Application.objects.filter(
        candidate=candidate
    ).select_related('job').order_by('-applied_at')

    return render(request, 'employees/application_status.html', {
        'applications': applications
    })


# =========================
# HR DASHBOARD
# =========================

def hr_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        return redirect('login')

    # Actual total jobs
    total_jobs = Job.objects.count()

    # Only normal candidates
    total_candidates = Candidate.objects.filter(
        user__is_staff=False
    ).count()

    # Actual total applications
    total_applications = Application.objects.count()

    # Shortlisted applications
    shortlisted = Application.objects.filter(
        status='Shortlisted'
    ).count()

    # Recent applications
    applications = Application.objects.select_related(
        'candidate__user',
        'job'
    ).order_by('-applied_at')[:10]

    return render(request, 'employees/hr_dashboard.html', {
        'total_jobs': total_jobs,
        'total_candidates': total_candidates,
        'total_applications': total_applications,
        'shortlisted': shortlisted,
        'applications': applications,
    })


# =========================
# CANDIDATE PROFILE
# =========================

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    candidate, created = Candidate.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'education': '',
            'skills': ''
        }
    )

    if request.method == 'POST':
        candidate.phone = request.POST.get('phone')
        candidate.education = request.POST.get('education')
        candidate.skills = request.POST.get('skills')

        if request.FILES.get('resume'):
            candidate.resume = request.FILES['resume']

        candidate.save()

        return redirect('candidate_dashboard')

    return render(request, 'employees/profile.html', {
        'candidate': candidate
    })



# =========================
# UPDATE APPLICATION STATUS - HR
# =========================

def update_application_status(request, application_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        return redirect('candidate_dashboard')

    application = get_object_or_404(
        Application,
        id=application_id
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        valid_statuses = [
            'Applied',
            'Shortlisted',
            'Rejected',
            'Selected'
        ]

        old_status = application.status

        if new_status in valid_statuses and new_status != old_status:

            application.status = new_status
            application.save()

            Notification.objects.create(
                candidate=application.candidate,
                message=(
                    f"Your application for "
                    f"{application.job.title} at "
                    f"{application.job.company} "
                    f"has been updated to {new_status}."
                )
            )

    return redirect('hr_dashboard')

# =========================
# HR CANDIDATES
# =========================

def hr_candidates(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    candidates = Candidate.objects.select_related(
        'user'
    ).filter(
        user__is_staff=False
    ).order_by('user__username')

    return render(request, 'employees/hr_candidates.html', {
        'candidates': candidates
    })


# =========================
# HR APPLICATIONS
# =========================

def hr_applications(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    applications = Application.objects.select_related(
        'candidate__user',
        'job'
    ).order_by('-applied_at')

    return render(request, 'employees/hr_applications.html', {
        'applications': applications
    })


# =========================
# SHORTLISTED APPLICATIONS
# =========================

def shortlisted_applications(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    applications = Application.objects.filter(
        status='Shortlisted'
    ).select_related(
        'candidate__user',
        'job'
    ).order_by('-applied_at')

    return render(request, 'employees/hr_shortlisted.html', {
        'applications': applications
    })


# =========================
# MANAGE JOBS
# =========================

def manage_jobs(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    jobs = Job.objects.all().order_by('-created_at')

    return render(request, 'employees/manage_jobs.html', {
        'jobs': jobs
    })


# =========================
# EDIT JOB
# =========================

def edit_job(request, job_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company = request.POST.get('company')
        job.description = request.POST.get('description')
        job.required_skills = request.POST.get('required_skills')
        job.experience = int(
            request.POST.get('experience') or 0
        )
        job.location = request.POST.get('location')
        job.salary = request.POST.get('salary')

        job.save()

        return redirect('manage_jobs')

    return render(request, 'employees/edit_job.html', {
        'job': job
    })


# =========================
# DELETE JOB
# =========================

def delete_job(request, job_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        job.delete()
        return redirect('manage_jobs')

    return redirect('manage_jobs')
# =========================
# SCHEDULE INTERVIEW
# =========================

def schedule_interview(request, application_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_staff:
        return redirect('candidate_dashboard')

    application = Application.objects.get(id=application_id)

    # Interview can be scheduled only for shortlisted candidate
    if application.status != 'Shortlisted':
        return redirect('hr_applications')

    if request.method == 'POST':
        interview_date = request.POST.get('interview_date')
        interview_time = request.POST.get('interview_time')
        interview_mode = request.POST.get('interview_mode')

        application.interview_date = interview_date
        application.interview_time = interview_time
        application.interview_mode = interview_mode
        application.interview_status = 'Scheduled'

        application.save()

        Notification.objects.create(
           candidate=application.candidate,
           message=f"Your interview for {application.job.title} has been scheduled."
        )

        return redirect('hr_applications')

    return render(request, 'employees/schedule_interview.html', {
        'application': application
    })
# =========================
# START AI INTERVIEW
# =========================

def start_ai_interview(request, application_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        return redirect('hr_dashboard')

    application = Application.objects.get(
        id=application_id,
        candidate__user=request.user
    )

    # Only shortlisted candidates can start
    if application.status != 'Shortlisted':
        return redirect('application_status')

    interview, created = AIInterview.objects.get_or_create(
        application=application
    )

    # Create questions only first time
    if created:
        skills = [
            skill.strip()
            for skill in application.job.required_skills.split(',')
            if skill.strip()
        ]

        questions = [
            f"Explain your experience with {skill}."
            for skill in skills[:3]
        ]

        questions += [
            f"Why are you suitable for the role of {application.job.title}?",
            "Tell us about a project you have worked on."
        ]

        for question in questions:
            AIInterviewQuestion.objects.create(
                interview=interview,
                question=question
            )

    return redirect(
        'ai_interview',
        interview_id=interview.id
    )
# =========================
# AI INTERVIEW
# =========================

def ai_interview(request, interview_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        return redirect('hr_dashboard')

    interview = AIInterview.objects.get(
        id=interview_id,
        application__candidate__user=request.user
    )

    question = interview.questions.filter(
        answer=''
    ).first()

    # All questions answered
    if question is None:
        return redirect(
            'ai_interview_result',
            interview_id=interview.id
        )

    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip()

        if answer:
            question.answer = answer

            # Basic automated scoring
            answer_words = set(
                word.lower().strip(".,!?")
                for word in answer.split()
            )

            required_skills = set(
                skill.strip().lower()
                for skill in interview.application.job.required_skills.split(',')
                if skill.strip()
            )

            matched_words = answer_words.intersection(
                required_skills
            )

            score = 0

            if len(answer_words) >= 10:
                score += 2

            if len(answer_words) >= 25:
                score += 2

            if matched_words:
                score += 6

            question.score = min(score, 10)
            question.save()

            return redirect(
                'ai_interview',
                interview_id=interview.id
            )

    total_questions = interview.questions.count()
    answered_questions = interview.questions.exclude(
        answer=''
    ).count()

    return render(request, 'employees/ai_interview.html', {
        'interview': interview,
        'question': question,
        'total_questions': total_questions,
        'answered_questions': answered_questions,
    })


# =========================
# AI INTERVIEW RESULT
# =========================

def ai_interview_result(request, interview_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        return redirect('hr_dashboard')

    interview = AIInterview.objects.get(
        id=interview_id,
        application__candidate__user=request.user
    )

    questions = interview.questions.all()

    total_score = sum(
        question.score
        for question in questions
    )

    max_score = questions.count() * 10

    if max_score > 0:
        percentage = round(
            (total_score / max_score) * 100
        )
    else:
        percentage = 0

    interview.total_score = percentage
    interview.completed = True
    interview.save()

    return render(request, 'employees/ai_interview_result.html', {
        'interview': interview,
        'questions': questions,
        'total_score': percentage,
    })


# =========================
# CANDIDATE NOTIFICATIONS
# =========================

def candidate_notifications(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        return redirect('hr_dashboard')

    candidate = get_object_or_404(
        Candidate,
        user=request.user
    )

    notifications = Notification.objects.filter(
        candidate=candidate
    ).order_by('-created_at')

    unread_count = notifications.filter(
        is_read=False
    ).count()

    return render(
        request,
        'employees/notifications.html',
        {
            'notifications': notifications,
            'unread_count': unread_count
        }
    )


# =========================
# MARK NOTIFICATION AS READ
# =========================

def mark_notification_read(request, notification_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        return redirect('hr_dashboard')

    candidate = get_object_or_404(
        Candidate,
        user=request.user
    )

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        candidate=candidate
    )

    notification.is_read = True
    notification.save()

    return redirect('candidate_notifications')