print("Loading forms.py")
from django import forms
from .models import Teacher, Student, Idea, TeamMember
from .models import Startup, StartupTeamMember


# Login Form
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Please Enter Team Lead Email / Founder'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Please Enter Your Password'}))
    
# Teacher Registration Form
class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['institute', 'name', 'email', 'mobile', 'gender', 'branch', 'teacher_id', 'id_card', 'password']

# Student Registration Form
class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email', 'mobile', 'gender', 'branch', 'institute', 'password']

# Idea Form
class IdeaForm(forms.ModelForm):
    team_leader_id_card = forms.FileField(required=True)  # Explicit file upload validation

    class Meta:
        model = Idea
        fields = ['title', 'academic_year', 'branch', 'domain', 'innovation_type', 'upload', 'team_leader_name', 'team_leader_email', 'team_leader_id_card']

# Team Member Form
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'email', 'id_card']

from .models import Prototype, PrototypeTeamMember

class PrototypeForm(forms.ModelForm):
    class Meta:
        model = Prototype
        fields = ['prototype_title', 'description', 'academic_year', 'branch', 'domain', 'innovation_type', 'problem', 
                  'solution', 'features', 'difference', 'video_url', 'team_size', 
                   'upload', 'mentor', 'develop_as_part', 'team_leader_name', 'team_leader_email', 'team_leader_id_card']

class PrototypeTeamMemberForm(forms.ModelForm):
    class Meta:
        model = PrototypeTeamMember
        fields = ['prototype_title', 'email', 'id_card']

class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = [
            'startup_name',
            'title',
            'website',
            'registration',
            'key_innovation',
            'incubation_year',
            'innovation_development',
            'sector',
            'innovation_type',
            'video_url',
            'innovation_image',
            'mentor',
            'team_leader_name',
            'team_leader_email',
            'team_leader_id_card'
        ]

class StartupTeamMemberForm(forms.ModelForm):
    class Meta:
        model = StartupTeamMember
        fields = ['name', 'email', 'id_card']

from django import forms

class EvaluationForm(forms.Form):
    quality_of_problems = forms.IntegerField(
        label="Quality of Problems",
        min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    awareness_of_background = forms.IntegerField(
        label="Awareness of Background",
        min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    technique_justification = forms.IntegerField(
        label="Technique Justification",
        min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    planning_scheduling = forms.IntegerField(
        label="Planning & Scheduling",
        min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    communication_clarity = forms.IntegerField(
        label="Communication Clarity",
        min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

from .models import Evaluation

SCORE_CHOICES = [(i, str(i)) for i in range(11)]  # 0 to 10

class EvaluationForm(forms.ModelForm):
    quality_of_problems = forms.TypedChoiceField(
        choices=SCORE_CHOICES,
        coerce=int,
        label='Quality of problem and clarity'
    )
    awareness_of_background = forms.TypedChoiceField(
        choices=SCORE_CHOICES,
        coerce=int,
        label='Awareness of background'
    )
    technique_justification = forms.TypedChoiceField(
        choices=SCORE_CHOICES,
        coerce=int,
        label='Selection and justification of techniques to be applied'
    )
    planning_scheduling = forms.TypedChoiceField(
        choices=SCORE_CHOICES,
        coerce=int,
        label='Project planning and scheduling'
    )
    communication_clarity = forms.TypedChoiceField(
        choices=SCORE_CHOICES,
        coerce=int,
        label='Clarity in written and oral communication'
    )

    class Meta:
        model = Evaluation
        fields = [
            'quality_of_problems',
            'awareness_of_background',
            'technique_justification',
            'planning_scheduling',
            'communication_clarity',
        ]