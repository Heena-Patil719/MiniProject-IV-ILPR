print("Loading views.py")


# Django core imports
from django.http import Http404
from django.core.exceptions import ValidationError

from django.http import HttpResponse
from .forms import EvaluationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.db.models import Avg
import logging

logger = logging.getLogger(__name__)
# Local app imports
from .models import Student, Teacher, Idea, TeamMember, Prototype, PrototypeTeamMember, Startup, StartupTeamMember, Evaluation, Project
from .forms import IdeaForm, TeamMemberForm, LoginForm, TeacherRegistrationForm, StudentRegistrationForm, StartupForm
from .utils import some_function
from django.http import JsonResponse
import json
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now   
from django.urls import reverse  # Yellow underline if unused



import random

# Temporary dictionary to store email verification codes
verification_codes = {}

# Login View
def login_view(request):
    if request.method == "POST":
        # Retrieve email and password from form
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Restrict login to only @gst.sies.edu.in emails
        if not email.endswith("@gst.sies.edu.in"):
            messages.error(request, "Only emails ending with @gst.sies.edu.in are allowed.")
            return redirect("login")  # Redirect back to login page

        user = None
        user_type = None

        # Check if the user is a student
        student = Student.objects.filter(email=email).first()
        if student and check_password(password, student.password):
            request.session['user_type'] = "student"
            request.session['user_id'] = student.student_id  # Use student_id from the database
            print(f"Logged in as Student: {student.name}, ID: {student.student_id}")  # Debugging
            return redirect("student_dashboard")  # Redirect to student dashboard

        # Check if the user is a teacher
        teacher = Teacher.objects.filter(email=email).first()
        if teacher and check_password(password, teacher.password):
            request.session["user_type"] = "teacher"
            request.session["user_id"] = teacher.id
            print(f"Logged in as Teacher: {teacher.name}, ID: {teacher.id}")  # Debugging
            return redirect("teacher_dashboard")  # Redirect to teacher dashboard

        # If no user matches, show error
        messages.error(request, "Invalid email or password.")

    # Render login form
    return render(request, "login.html", {"form": LoginForm()})

# Choose Role View
def choose_role(request):
    return render(request, 'choose_role.html')

# Teacher Registration View
def teacher_register(request):
    # Initialize the form with POST data and uploaded files
    form = TeacherRegistrationForm(request.POST or None, request.FILES or None)

    
    if request.method == "POST":
        email = request.POST.get("email")

        # Backend email validation
        if not email.endswith("@gst.sies.edu.in"):
            messages.error(request, "Email must end with @gst.sies.edu.in")
            return render(request, "teacher_registration.html", {"form": form})

        # Validate the form data
        if form.is_valid():
            # Save the teacher instance
            teacher = form.save(commit=False)
            # Hash the password for security
            teacher.password = make_password(form.cleaned_data['password'])
            # Save the teacher object in the database
            teacher.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")

    # Render the registration page with the form
    return render(request, "teacher_registration.html", {"form": form})

# Student Registration View
def register(request):
    form = StudentRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        student = form.save(commit=False)
        student.password = make_password(form.cleaned_data['password'])
        student.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')
    return render(request, 'registration.html', {'form': form})

# Forgot Password View
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = Student.objects.filter(email=email).first() or Teacher.objects.filter(email=email).first()
        if user:
            verification_code = str(random.randint(100000, 999999))
            request.session["verification_code"] = verification_code
            request.session["reset_email"] = email
            send_mail(
                "Your Verification Code",
                f"Your verification code is {verification_code}",
                "no-reply@example.com",
                [email]
            )
            messages.success(request, "Verification code sent! Please enter the code below.")
            return redirect("verify_code")
        messages.error(request, "Email not found!")
    return render(request, "forgot_password.html")

# Reset Password Confirmation View
def reset_password(email, new_password):
    try:
        print(f"Reset attempt for email: {email}")

        # Check Teacher database
        teacher = Teacher.objects.filter(email=email).first()
        if teacher:
            print(f"Teacher found: {teacher.email}")
            teacher.password = make_password(new_password)  # Hash the password
            teacher.reset_token = None  # Clear reset token
            teacher.reset_token_expires = None
            teacher.save()  # Save changes
            print(f"Password updated for Teacher: {teacher.email}")
            return "Password updated successfully for Teacher.", True

        # Check Student database
        student = Student.objects.filter(email=email).first()
        if student:
            print(f"Student found: {student.email}")
            student.password = make_password(new_password)  # Hash the password
            student.reset_token = None  # Clear reset token
            student.reset_token_expires = None
            student.save()  # Save changes
            print(f"Password updated for Student: {student.email}")
            return "Password updated successfully for Student.", True

        print("Email not found in the database.")
        return "Email not found in the database.", False

    except Exception as e:
        print(f"Error during password reset: {str(e)}")
        return f"An error occurred: {str(e)}", False
    

def reset_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Debugging logs to check what data is being posted
        print(f"Email: {email}, New Password: {new_password}, Confirm Password: {confirm_password}")

        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            print("Password mismatch detected.")
            return render(request, "reset_password.html", {"email": email})  # Keeps email in the form for convenience

        # Call the reset_password function to update the password
        response_message, success = reset_password(email, new_password)
        
        # Debugging logs to confirm success or failure
        print(f"Reset Password Response: {response_message}, Success: {success}")

        if success:
            messages.success(request, response_message)
            return redirect("login")  # Redirect to login on successful reset
        else:
            messages.error(request, response_message)
            print("Password reset failed, staying on reset page.")
            return render(request, "reset_password.html", {"email": email})  # Keeps email in the form for retry

    # Render the reset password form for GET requests or failed POST attempts
    return render(request, "reset_password.html")

# Verify Code View
def verify_code(request):
    if request.method == "POST":
        entered_code = request.POST.get("verification_code")
        email = request.session.get("reset_email")
        stored_code = request.session.get("verification_code")

        if email and stored_code and entered_code == stored_code:
            request.session["verified_email"] = email
            del request.session["verification_code"]
            messages.success(request, "Code verified! Please reset your password.")
            return redirect("reset_password")
        messages.error(request, "Invalid verification code.")
    return render(request, "verify_code.html")

def student_dashboard(request):
    if request.session.get('user_type') != 'student':
        return redirect('login')

    # You can use session data like:
    student_id = request.session.get('user_id')

    context = {
        'student_id': student_id,
        'performance_data': {
            'students': 100,
            'total_projects': 50,
            'ideas': 15,
            'prototypes': 25,
            'startups': 10
        }
    }
    return render(request, 'student_dashboard.html', context)

def teacher_dashboard(request):
    # Fetch the logged-in teacher's ID from session
    teacher_id = request.session.get("user_id")
    if not teacher_id:
        return redirect('login')  # Redirect if not logged in

    # Get the teacher object
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # Fetch total number of students
    total_students = Student.objects.count()

    # Count projects from individual tables assigned to this teacher
    num_ideas = Idea.objects.filter(mentor=teacher.name).count()
    num_prototypes = Prototype.objects.filter(mentor=teacher.name).count()
    num_startups = Startup.objects.filter(mentor=teacher.name).count()

    # Total projects assigned to this mentor
    total_projects = num_ideas + num_prototypes + num_startups

    # Evaluations done by this mentor
    total_evaluated = Evaluation.objects.filter(mentor_name=teacher.name).count()
    total_remaining = total_projects - total_evaluated

    # Debugging Output
    print(f"Total Students: {total_students}")
    print(f"Total Projects for {teacher.name}: {total_projects} (Ideas: {num_ideas}, Prototypes: {num_prototypes}, Startups: {num_startups})")
    print(f"Total Evaluated: {total_evaluated}, Remaining: {total_remaining}")

    # Prepare the context data
    context = {
        'teacher': teacher,
        'performance_data': {
            'students': total_students,
            'total_projects': total_projects,
            'ideas': num_ideas,
            'prototypes': num_prototypes,
            'startups': num_startups,
            'total_evaluations': total_evaluated,
        },
        'evaluation_chart_data': {
            'evaluated': total_evaluated,
            'remaining': total_remaining
        }
    }

    return render(request, 'teacher_dashboard.html', context)
def start_up(request):
    teachers = Teacher.objects.all()
    return render(request, 'start_up.html', {'teachers': teachers})

def idea_form(request):
    teachers = Teacher.objects.all()
    return render(request, 'idea_form.html', {'teachers': teachers})

def prototype_form(request):
    teachers = Teacher.objects.all()
    return render(request, 'prototype_form.html', {'teachers': teachers})

# Idea Submission
def idea_submission(request):
    if request.method == 'POST':
        idea_form = IdeaForm(request.POST, request.FILES)
        team_count = int(request.POST.get('team_count', 0))
        team_member_forms = []

        for i in range(1, team_count + 1):
            team_member_data = {
                'name': request.POST.get(f'team_member_{i}_name'),
                'email': request.POST.get(f'team_member_{i}_email'),
                'id_card': request.FILES.get(f'team_member_{i}_id_card'),
            }
            team_member_forms.append(TeamMemberForm(team_member_data))

        if idea_form.is_valid() and all(form.is_valid() for form in team_member_forms):
            idea = idea_form.save()
            for form in team_member_forms:
                team_member = form.save(commit=False)
                team_member.idea = idea
                team_member.save()

            messages.success(request, "Idea and team members saved successfully!")
            return redirect('idea_success')  # Redirect to idea_success.html

    else:
        idea_form = IdeaForm()

    return render(request, 'idea_form.html', {'idea_form': idea_form})


from django.shortcuts import render, redirect
from .models import Idea, TeamMember

def submit_idea(request):
    if request.method == 'POST':
        try:
            # Extract form data
            title = request.POST.get('title')
            academic_year = request.POST.get('academic_year')
            branch = request.POST.get('branch')
            domain = request.POST.get('domain')
            innovation_type = request.POST.get('innovation_type')
            status_level = request.POST.get('status_level')
            problem = request.POST.get('problem')
            solution = request.POST.get('solution')
            features = request.POST.get('features')
            difference = request.POST.get('difference')
            video_url = request.POST.get('video_url')
            develop_as_part = request.POST.get('develop_as_part')
            mentor = request.POST.get('mentor')
            team_leader_name = request.POST.get('team_leader_name')
            team_leader_email = request.POST.get('team_leader_email')
            team_count = int(request.POST.get('team_count', 0))

            # Handle file uploads
            upload = request.FILES.get('upload', None)
            team_leader_id_card = request.FILES.get('team_leader_id_card', None)

            # Validate required fields
            if not all([title, academic_year, branch, domain, innovation_type, status_level, problem, solution,
                        features, difference, video_url, develop_as_part, mentor, team_leader_name, team_leader_email]):
                messages.error(request, "Please fill in all required fields.")
                return redirect('idea_form')

            # Create the Idea instance
            idea = Idea.objects.create(
                title=title,
                academic_year=academic_year,
                branch=branch,
                domain=domain,
                innovation_type=innovation_type,
                status_level=status_level,
                problem=problem,
                solution=solution,
                features=features,
                difference=difference,
                video_url=video_url,
                develop_as_part=develop_as_part,
                mentor=mentor,
                team_leader_name=team_leader_name,
                team_leader_email=team_leader_email,
                upload=upload,
                team_leader_id_card=team_leader_id_card,
                team_size=team_count + 1  # Include team leader in team size
            )

            # Save team members
            for i in range(1, team_count + 1):
                name = request.POST.get(f'team_member_{i}_name')
                email = request.POST.get(f'team_member_{i}_email')
                id_card = request.FILES.get(f'team_member_{i}_id_card')

                if name and email and id_card:
                    # Ensure email uniqueness
                    if not TeamMember.objects.filter(email=email).exists():
                        TeamMember.objects.create(
                            name=name,
                            email=email,
                            id_card=id_card,
                            project=idea  # Link to the Idea instance
                        )
                    else:
                        messages.warning(request, f"Team member {i} with email {email} already exists and was skipped.")

            # Success message
            messages.success(request, "Idea and team members saved successfully!")
            return redirect('idea_success')  # Redirect to success page

        except Exception as e:
            # Log the error and show a user-friendly message
            print(f"Error saving idea: {str(e)}")
            messages.error(request, "An unexpected error occurred while saving your idea. Please try again.")
            return redirect('idea_form')

    # Render the form for GET requests
    teachers = Teacher.objects.all()
    return render(request, 'idea_form.html', {'teachers': teachers})



def idea_success(request):
    return render(request, 'idea_success.html')

def verify_email(request):
    return HttpResponse("Email verification page")

def save_idea(request):
    return HttpResponse("Idea saved successfully!")

def student_projects(request):
    # Fetch data from all three models
    ideas = Idea.objects.all()
    prototypes = Prototype.objects.all()
    startups = Startup.objects.all()

    # Combine data from all models into a single list
    projects = []

    # Add data from Idea model
    for idea in ideas:
        projects.append({
            'type': 'Idea',  # Project type
            'project_name': idea.title,
            'branch': idea.branch,
            'team_leader': idea.team_leader_name,
            'mentor': idea.mentor,
            'details': {
                'title': idea.title,
                'academic_year': idea.academic_year,
                'domain': idea.domain,
                'innovation_type': idea.innovation_type,
                'problem': idea.problem,
                'solution': idea.solution,
                'features': idea.features,
                'difference': idea.difference,
                'video_url': idea.video_url,
                'team_size': idea.team_size,
                'idea_description': idea.idea_description,
                'project_stage': idea.project_stage,
                'upload': idea.upload.url if idea.upload else None,
                'develop_as_part': idea.develop_as_part,
                'team_leader_email': idea.team_leader_email,
                'team_leader_id_card': idea.team_leader_id_card.url if idea.team_leader_id_card else None,
                'team_members': [
                    {
                        'name': member.name,
                        'email': member.email,
                        'id_card': member.id_card.url if member.id_card else None
                    }
                    for member in idea.team_members.all()
                ]
            }
        })

    # Add data from Prototype model
    for prototype in prototypes:
        projects.append({
            'type': 'Prototype',  # Project type
            'project_name': prototype.prototype_title,
            'branch': prototype.branch,
            'team_leader': prototype.team_leader_name,
            'mentor': prototype.mentor,
            'details': {
                'prototype_title': prototype.prototype_title,
                'description': prototype.description,
                'academic_year': prototype.academic_year,
                'domain': prototype.domain,
                'innovation_type': prototype.innovation_type,
                'problem': prototype.problem,
                'solution': prototype.solution,
                'features': prototype.features,
                'difference': prototype.difference,
                'video_url': prototype.video_url,
                'team_size': prototype.team_size,
                'status_level': prototype.status_level,
                'prototype_files': prototype.prototype_files.url if prototype.prototype_files else None,
                'upload': prototype.upload.url if prototype.upload else None,
                'develop_as_part': prototype.develop_as_part,
                'team_leader_email': prototype.team_leader_email,
                'team_leader_id_card': prototype.team_leader_id_card.url if prototype.team_leader_id_card else None,
                'team_members': [
                    {
                        'name': member.team_leader_name,  # Use team_leader_name instead of name
                        'email': member.email,
                        'id_card': member.id_card.url if member.id_card else None
                    }
                    for member in prototype.prototype_team_members.all()
                ]
            }
        })

    # Add data from Startup model
    for startup in startups:
        projects.append({
            'type': 'Startup',  # Project type
            'project_name': startup.startup_name,
            'branch': startup.branch,
            'team_leader': startup.team_leader_name,
            'mentor': startup.mentor,
            'details': {
                'startup_name': startup.startup_name,
                'title': startup.title,
                'website': startup.website,
                'incubation_year': startup.incubation_year,
                'innovation_development': startup.innovation_development,
                'sector': startup.sector,
                'innovation_type': startup.innovation_type,
                'video_url': startup.video_url,
                'mentor': startup.mentor,
                'team_leader_email': startup.team_leader_email,
                'team_leader_id_card': startup.team_leader_id_card.url if startup.team_leader_id_card else None,
                'team_members': [
                    {
                        'name': member.name,
                        'email': member.email,
                        'id_card': member.id_card.url if member.id_card else None
                    }
                    for member in startup.team_members.all()
                ]
            }
        })

    # Fetch all teachers (mentors) from the database
    mentors = Teacher.objects.values_list('name', flat=True).distinct()

    # Pass the combined data and mentors to the template
    context = {
        'projects': projects,
        'mentors': mentors,  # Pass mentors to the template
    }
    return render(request, 'student_projects.html', context)

def student_groups(request):
    return HttpResponse("Student groups page")

from django.shortcuts import render, get_object_or_404
from .models import Idea, Prototype, Startup
from django.http import JsonResponse

from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def project_detail(request, project_type, project_id):
    # Determine which model to query based on project_type
    if project_type == 'idea':
        model = Idea
        title_field = 'title'
        team_member_relation = 'team_members'  # Related name for Idea's team members
    elif project_type == 'prototype':
        model = Prototype
        title_field = 'prototype_title'
        team_member_relation = 'prototype_team_members'  # Related name for Prototype's team members
    elif project_type == 'startup':
        model = Startup
        title_field = 'startup_name'
        team_member_relation = 'team_members'  # Related name for Startup's team members
    else:
        return JsonResponse({'error': 'Invalid project type'}, status=400)

    # Fetch the project from the database
    project = get_object_or_404(model, id=project_id)

    # Prepare the data to be sent as JSON
    data = {}

    if project_type in ['idea', 'prototype']:
        # Handle Idea and Prototype models with generic field retrieval
        data = {
            'id': project.id,
            'title': getattr(project, title_field, 'N/A'),
            'academic_year': getattr(project, 'academic_year', 'N/A'),
            'branch': getattr(project, 'branch', 'N/A'),
            'domain': getattr(project, 'domain', 'N/A'),
            'innovation_type': getattr(project, 'innovation_type', 'N/A'),
            'status_level': getattr(project, 'status_level', 'N/A'),
            'problem': getattr(project, 'problem', 'N/A'),
            'solution': getattr(project, 'solution', 'N/A'),
            'features': getattr(project, 'features', 'N/A'),
            'difference': getattr(project, 'difference', 'N/A'),
            'video_url': getattr(project, 'video_url', None),
            'team_size': getattr(project, 'team_size', 'N/A'),
            'mentor': getattr(project, 'mentor', 'N/A'),
            'develop_as_part': getattr(project, 'develop_as_part', 'N/A'),
            'upload': project.upload.url if hasattr(project, 'upload') and project.upload else None,
            'team_leader_name': getattr(project, 'team_leader_name', 'N/A'),
            'team_leader_email': getattr(project, 'team_leader_email', 'N/A'),
            'team_leader_id_card': project.team_leader_id_card.url if hasattr(project, 'team_leader_id_card') and project.team_leader_id_card else None,
        }
    elif project_type == 'startup':
        # Handle Startup model with custom field mapping
        data = {
            'id': project.id,
            'title': getattr(project, title_field, 'N/A'),  # startup_name mapped to title
            'sector': getattr(project, 'sector', 'N/A'),
            'registration': getattr(project, 'registration', 'N/A'),
            'key_innovation': getattr(project, 'key_innovation', 'N/A'),
            'incubation_year': getattr(project, 'incubation_year', 'N/A'),
            'innovation_development': getattr(project, 'innovation_development', 'N/A'),
            'status_level': getattr(project, 'status_level', 'N/A'),
            'video_url': getattr(project, 'video_url', None),
            'mentor': getattr(project, 'mentor', 'N/A'),
            'team_leader_name': getattr(project, 'team_leader_name', 'N/A'),
            'team_leader_email': getattr(project, 'team_leader_email', 'N/A'),
            'team_leader_id_card': project.team_leader_id_card.url if hasattr(project, 'team_leader_id_card') and project.team_leader_id_card else None,
            'team_count': getattr(project, 'team_count', 'N/A'),
            'innovation_image': project.innovation_image.url if hasattr(project, 'innovation_image') and project.innovation_image else None,
        }

    # Fetch team members for the project (common logic for all project types)
    team_members = []
    if hasattr(project, team_member_relation):
        for member in getattr(project, team_member_relation).all():
            team_members.append({
                'name': member.name or 'N/A',
                'email': member.email or 'N/A',
                'id_card': member.id_card.url if member.id_card else 'N/A',
            })
    data['team_members'] = team_members

    # Return the JSON response
    return JsonResponse(data)

def validate_mobile(request):
    mobile = request.GET.get('mobile')
    exists = Teacher.objects.filter(mobile=mobile).exists()
    return JsonResponse({'exists': exists})

def validate_prn(request):
    prn = request.GET.get('prn')
    exists = Student.objects.filter(student_id=prn).exists()
    return JsonResponse({'exists': exists})

def validate_teacher_id(request):
    teacher_id = request.GET.get("teacher_id", "").strip()
    exists = Teacher.objects.filter(teacher_id=teacher_id).exists()
    return JsonResponse({"exists": exists})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Prototype, PrototypeTeamMember, Teacher

def prototype_form(request):
    if request.method == "POST":
        return submit_prototype(request)
    return render(request, 'prototype_form.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Prototype, PrototypeTeamMember
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Prototype, PrototypeTeamMember
def submit_prototype(request):
    if request.method == 'POST':
        try:
            # Extract form data
            prototype_title = request.POST.get('prototype_title')
            description = request.POST.get('problem')  # Using problem as description
            branch = request.POST.get('branch')
            domain = request.POST.get('domain')
            innovation_type = request.POST.get('innovation_type')
            problem = request.POST.get('problem')
            solution = request.POST.get('solution')
            features = request.POST.get('features')
            difference = request.POST.get('difference')
            video_url = request.POST.get('video_url')
            status_level = request.POST.get('status_level')
            develop_as_part = request.POST.get('develop_as_part')
            academic_year = request.POST.get('academic_year')
            
            # Get files
            prototype_files = request.FILES.get('prototype_files')
            
            # Get mentor ID and convert to name
            mentor_id = request.POST.get('mentor')
            try:
                from project_repo.models import Teacher  # Replace with your actual model name
                mentor_obj = Teacher.objects.get(id=mentor_id)
                mentor_name = mentor_obj.name  # Get the actual name
            except Exception as e:
                # Fallback if mentor not found
                mentor_name = f"Mentor ID: {mentor_id}"
            
            team_leader_name = request.POST.get('team_leader_name')
            team_leader_email = request.POST.get('team_leader_email')
            team_leader_id_card = request.FILES.get('team_leader_id_card')
            team_count = int(request.POST.get('team_count', 0))

            # Validate required fields
            if not all([prototype_title, branch, domain, innovation_type, problem, solution,
                        features, difference, video_url, mentor_id, team_leader_name, team_leader_email]):
                messages.error(request, "Missing required fields.")
                return redirect('prototype_form')

            # Validate file sizes
            if prototype_files and prototype_files.size > 200 * 1024 * 1024:  # 200MB
                messages.error(request, "Uploaded prototype file exceeds 200MB limit.")
                return redirect('prototype_form')
            if team_leader_id_card and team_leader_id_card.size > 2 * 1024 * 1024:  # 2MB
                messages.error(request, "ID Card file exceeds 2MB limit.")
                return redirect('prototype_form')

            # Calculate team size
            team_size = team_count + 1  # Include the team leader

            # Create Prototype instance
            prototype = Prototype.objects.create(
                user=request.user,  # Make sure the user is logged in
                prototype_title=prototype_title,
                description=description,
                branch=branch,
                domain=domain,
                innovation_type=innovation_type,
                problem=problem,
                solution=solution,
                features=features,
                difference=difference,
                video_url=video_url,
                upload=prototype_files,  # Use upload field as per model
                prototype_files=prototype_files,  # Also set prototype_files to be safe
                mentor=mentor_name,  # Store the name instead of ID
                team_leader_name=team_leader_name,
                team_leader_email=team_leader_email,
                team_leader_id_card=team_leader_id_card,
                team_size=team_size,
                team_count=team_count,
                status_level=status_level,
                develop_as_part=develop_as_part,
                academic_year=academic_year
            )

            # Save team members
            for i in range(1, team_count + 1):
                member_name = request.POST.get(f'team_member_{i}_name')
                member_email = request.POST.get(f'team_member_{i}_email')
                member_id_card = request.FILES.get(f'team_member_{i}_id_card')

                if member_name and member_email:
                    PrototypeTeamMember.objects.create(
                        project=prototype,  # Use 'project' as per model definition
                        name=member_name,
                        email=member_email,
                        id_card=member_id_card
                    )

            # Success message and redirection
            messages.success(request, "Prototype submitted successfully!")
            return redirect('projects')  # Redirect to the projects page

        except ValidationError as ve:
            # Handle validation errors
            messages.error(request, str(ve))
            return redirect('prototype_form')

        except Exception as e:
            # Log the error and show a user-friendly message
            import traceback
            print(f"Error during prototype submission: {e}")
            print(traceback.format_exc())
            messages.error(request, f"An error occurred while submitting the prototype: {str(e)}")
            return redirect('prototype_form')

    # If not POST, render the form
    return render(request, 'prototype_form.html')

def submit_business(request):
    if request.method == "POST":
        form = StartupForm(request.POST, request.FILES)
        action = request.POST.get("action")  # Get the action from the submitted form

        if form.is_valid():
            # Save the startup information
            startup = form.save(commit=False)

            # Fetch the mentor's name using the mentor ID
            mentor_id = request.POST.get("mentor")
            try:
                mentor = Teacher.objects.get(id=mentor_id)  # Fetch the mentor object
                startup.mentor = mentor.name  # Save the mentor's name
            except Teacher.DoesNotExist:
                messages.error(request, "Invalid mentor selected.")
                return render(request, "start_up.html", {"form": form})

            startup.team_leader_email = request.POST.get('team_leader_email')
            startup.save()

            # Handle Team Members
            team_count = int(request.POST.get("team_count", 0))
            for i in range(1, team_count + 1):
                name = request.POST.get(f"team_member_{i}_name")
                email = request.POST.get(f"team_member_{i}_email")
                id_card = request.FILES.get(f"team_member_{i}_id_card")

                if name and email and id_card:
                    StartupTeamMember.objects.create(
                        startup=startup,
                        name=name,
                        email=email,
                        id_card=id_card
                    )

            # Differentiate between "Save and Next" and "Submit"
            if action == "save_next":
                messages.success(request, "Startup information saved successfully! Proceed to the next step.")
                return redirect("projects")  # Redirect to the next step page
            elif action == "submit":
                messages.success(request, "Startup and team members saved successfully!")
                return redirect("Projects")  # Redirect to the success page
        else:
            # Debug: Print form errors
            print(form.errors)
            messages.error(request, "Form submission failed. Please check the errors.")
            return render(request, "start_up.html", {"form": form})

    else:
        form = StartupForm()

    return render(request, "start_up.html", {"form": form})


def success_page(request):
    return render(request, 'success.html')


from django.shortcuts import render, redirect
from .models import Idea, Prototype, Startup, Student, Teacher

def projects(request):
    # Check if the user is logged in using session variables
    user_type = request.session.get("user_type")
    user_id = request.session.get("user_id")

    # Redirect to login if session variables are missing
    if not user_type or not user_id:
        return redirect("login")

    # Initialize user_email as None
    user_email = None

    # Fetch user_email based on user_type
    if user_type == "student":
        student = Student.objects.filter(student_id=user_id).first()
        user_email = student.email if student else None

    elif user_type == "teacher":
        teacher = Teacher.objects.filter(id=user_id).first()
        user_email = teacher.email if teacher else None

    # Debugging: Print user_email to verify it's being set correctly
    print(f"User Email: {user_email}")

    # Ensure user_email is valid before querying the database
    if not user_email:
        return render(request, 'Projects.html', {
            'ideas': [],
            'prototypes': [],
            'startups': [],
        })

    # Fetch ideas, prototypes, and startups submitted by the logged-in user
    ideas = Idea.objects.filter(team_leader_email=user_email)
    prototypes = Prototype.objects.filter(team_leader_email=user_email)
    startups = Startup.objects.filter(team_leader_email=user_email)

    # Debugging: Print fetched data to verify queries are working
    print(f"Fetched Ideas: {list(ideas)}")
    print(f"Fetched Prototypes: {list(prototypes)}")
    print(f"Fetched Startups: {list(startups)}")

    # Render the template with the fetched data
    return render(request, 'Projects.html', {
        'ideas': ideas,
        'prototypes': prototypes,
        'startups': startups,
    })

def profile(request):
    # Fetch the logged-in teacher's ID from the session
    teacher_id = request.session.get("user_id")
    if not teacher_id:
        return redirect('login')  # Redirect to login if not authenticated

    # Get the teacher object
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # Fetch mentors associated with the teacher's projects
    # Replace the previous query with the correct logic
    mentors = Project.objects.filter(teacher=teacher).values_list('teacher__name', flat=True).distinct()

    context = {
        'teacher': teacher,
        'mentors': mentors,  # Mentor list associated with the teacher
    }
    return render(request, 'profile.html', context)


def contact(request):
    return render(request, 'contact.html')  # Ensure you have a contact.html template

def about_us(request):
    return render(request, 'about_us.html')  # Ensure you have an about_us.html template


def edit_prototype(request, prototype_id):
    # Fetch the prototype based on its ID
    prototype = get_object_or_404(Prototype, id=prototype_id)
    if request.method == 'POST':
        # Save updated fields from the form submission
        prototype.prototype_title = request.POST.get('prototype_title')
        prototype.description = request.POST.get('description')
        prototype.branch = request.POST.get('branch')
        prototype.domain = request.POST.get('domain')
        prototype.innovation_type = request.POST.get('innovation_type')
        prototype.problem = request.POST.get('problem')
        prototype.solution = request.POST.get('solution')
        prototype.features = request.POST.get('features')
        prototype.difference = request.POST.get('difference')
        prototype.team_size = request.POST.get('team_size')
        prototype.status_level = request.POST.get('status_level')
        prototype.save()
        # Redirect to the projects page
        return redirect('projects')  # Ensure this matches the URL name
    # Render the edit form with the current prototype details
    return render(request, 'edit_prototype_form.html', {'prototype': prototype})



def student_profile(request):
    student_id = request.session.get("user_id")
    if not student_id:
        return redirect('login')

    # Fetch the logged-in student's details
    student = get_object_or_404(Student, student_id=student_id)

    # Use the correct field to fetch the team leader's ID card
    idea_id_card = Idea.objects.filter(team_leader_id_card=student_id).values_list('team_leader_id_card', flat=True).first()
    prototype_id_card = Prototype.objects.filter(team_leader_id_card=student_id).values_list('team_leader_id_card', flat=True).first()
    startup_id_card = Startup.objects.filter(team_leader_id_card=student_id).values_list('team_leader_id_card', flat=True).first()

    # Determine the ID card to display (prioritize Idea > Prototype > Startup)
    displayed_id_card = idea_id_card or prototype_id_card or startup_id_card

    # Determine if the ID card is an image
    is_image = displayed_id_card and displayed_id_card.endswith((".png", ".jpg", ".jpeg"))

    context = {
        'student': student,
        'displayed_id_card': displayed_id_card,  # Single ID card to show
        'is_image': is_image,  # Pass whether it's an image to the template
    }
    return render(request, 'student_profile.html', context)

def display_team_leader_id_card(request):
    idea_team_leader_id_card = Idea.objects.values_list('team_leader_id_card', flat=True).first()
    prototype_team_leader_id_card = Prototype.objects.values_list('team_leader_id_card', flat=True).first()
    startup_team_leader_id_card = Startup.objects.values_list('team_leader_id_card', flat=True).first()

    context = {
        'idea_id_card': idea_team_leader_id_card,
        'prototype_id_card': prototype_team_leader_id_card,
        'startup_id_card': startup_team_leader_id_card,
    }
    return render(request, 'team_leader_id_card.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Idea, Prototype, Startup, Evaluation, Teacher

def teacher_evaluations(request):
    print("LOGGED-IN USER:", request.user.username)
    # Get the logged-in teacher's ID from the session
    teacher_id = request.session.get("user_id")
    print(f"Teacher ID from session: {teacher_id}")  # Debugging

    if not teacher_id:
        print("No teacher ID found in session.")  # Debugging
        return redirect('login')  # Redirect to login if not authenticated

    # Fetch the logged-in teacher from the Teacher model
    try:
        teacher = get_object_or_404(Teacher, id=teacher_id)
        logged_in_teacher_name = teacher.name
        print(f"Fetched Teacher: {teacher.name}")  # Debugging
    except Teacher.DoesNotExist:
        print("Teacher with given ID does not exist.")  # Debugging
        return redirect('login')  # Redirect to login if teacher does not exist

    # Fetch all projects
    idea_projects = Idea.objects.all()
    prototype_projects = Prototype.objects.all()
    startup_projects = Startup.objects.all()

    # Check if projects have been evaluated by the logged-in teacher
    for project in idea_projects:
        # Check if this teacher has evaluated this project
        project.evaluated = Evaluation.objects.filter(project_id=project.id, teacher=teacher).exists()
    for project in prototype_projects:
        project.evaluated = Evaluation.objects.filter(project_id=project.id, teacher=teacher).exists()
    for project in startup_projects:
        project.evaluated = Evaluation.objects.filter(project_id=project.id, teacher=teacher).exists()

    # Pass the logged-in teacher's name and evaluated status to the template
    context = {
        'idea_projects': idea_projects,
        'prototype_projects': prototype_projects,
        'startup_projects': startup_projects,
        'logged_in_teacher_name': logged_in_teacher_name,  # Logged-in teacher's name
    }

    return render(request, 'teacher_evaluations.html', context)
    

    return render(request, 'teacher_evaluations.html', context)

def toggle_evaluation(request, project_id):
    if request.method == 'POST':
        print(f"Toggle evaluation for project ID: {project_id}")  # Debugging
        for model in [Idea, Prototype, Startup]:
            try:
                project = model.objects.get(id=project_id)
                print(f"Found project: {project.title}")  # Debugging
                project.evaluated = True  # Mark as evaluated
                project.save()
                break
            except model.DoesNotExist:
                continue
    return redirect('evaluated_projects')  


def evaluated_project(request, project_type, project_id):
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)

            # Set the project_type from URL argument
            evaluation.project_type = project_type

            # Calculate total and average
            total = (
                evaluation.quality_of_problems +
                evaluation.awareness_of_background +
                evaluation.technique_justification +
                evaluation.planning_scheduling +
                evaluation.communication_clarity
            )
            evaluation.total_marks = total
            evaluation.average = total / 5

            evaluation.save()
            messages.success(request, "Project evaluation submitted successfully!")
            return redirect('evaluation_success')
    else:
        form = EvaluationForm()

    return render(request, 'evaluated_project.html', {'form': form})

def evaluated_project(request, project_type, project_id):
    teacher_id = request.session.get("user_id")
    if not teacher_id:
        return redirect("login")

    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        raise Http404("Teacher not found")

    if project_type == 'idea':
        project = get_object_or_404(Idea, id=project_id)
        project_name = project.title
    elif project_type == 'prototype':
        project = get_object_or_404(Prototype, id=project_id)
        project_name = project.prototype_title
    elif project_type == 'startup':
        project = get_object_or_404(Startup, id=project_id)
        project_name = project.title
    else:
        raise Http404("Invalid project type")

    already_evaluated = Evaluation.objects.filter(
        teacher=teacher, project_id=project.id, project_type=project_type
    ).exists()

    if already_evaluated:
        messages.warning(request, "You have already evaluated this project.")
        return redirect("evaluation_details", project_type=project_type, project_id=project.id)

    if request.method == "POST":
        form = EvaluationForm(request.POST)
        if form.is_valid():
            Evaluation.objects.create(
                project_name=project_name,
                team_leader_name=project.team_leader_name,
                mentor_name=teacher.name,
                quality_of_problems=form.cleaned_data['quality_of_problems'],
                awareness_of_background=form.cleaned_data['awareness_of_background'],
                technique_justification=form.cleaned_data['technique_justification'],
                planning_scheduling=form.cleaned_data['planning_scheduling'],
                communication_clarity=form.cleaned_data['communication_clarity'],
                project_type=project_type,
                project_id=project.id,
                teacher=teacher
            )
            messages.success(request, "Evaluation submitted successfully!")
            return redirect("evaluated_project", project_type=project_type, project_id=project.id)
    else:
        form = EvaluationForm()

    return render(request, "evaluated_project.html", {
        "project": project,
        "project_name": project_name,
        "mentor": teacher.name,
        "project_type": project_type.capitalize(),
        "form": form,
        "already_evaluated": already_evaluated,
    })

def evaluation_details(request, project_type, project_id):
    teacher_id = request.session.get("user_id")
    if not teacher_id:
        return redirect("login")

    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        raise Http404("Teacher not found")

    # Fetch the evaluation record for the given project, project type, and teacher
    evaluation = get_object_or_404(Evaluation, project_type=project_type, project_id=project_id, teacher=teacher)

    return render(request, "evaluation_details.html", {
        "evaluation": evaluation,
        "total_marks": evaluation.total_marks,
        "average_marks": evaluation.average,
    })

def get_teachers(request):
    teachers = Teacher.objects.all().values('id', 'name')
    return JsonResponse(list(teachers), safe=False)