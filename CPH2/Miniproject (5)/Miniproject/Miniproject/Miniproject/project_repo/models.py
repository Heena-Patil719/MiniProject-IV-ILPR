print("Loading models.py")

# Existing code
from django.db import models

from django.contrib.auth.hashers import make_password, is_password_usable
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import User  # Import User model
from .utils import some_function




# Validator for file types
def validate_file_type(value):
    if not value.name.endswith(('.png', '.jpg', '.jpeg', '.pdf')):
        raise ValidationError(f"Invalid file type for {value.name}. Accepted formats: PNG, JPG, PDF.")

def validate_id_card_size(value):
    max_size = 2 * 1024 * 1024  # 2MB
    if value.size > max_size:
        raise ValidationError("ID Card file must be less than 2MB.")

# General PDF max size 200MB
def validate_pdf_size(value):
    max_size = 200 * 1024 * 1024  # 200MB
    if value.size > max_size:
        raise ValidationError("Uploaded PDF file must be less than 200MB.")

# Gender Choices
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

# Function to get academic year dynamically
def get_current_academic_year():
    current_year = datetime.now().year
    return f"{current_year}-{current_year + 1}"

# Teacher Model
class Teacher(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    branch = models.CharField(max_length=100)
    teacher_id = models.CharField(unique=True, max_length=50)
    institute = models.CharField(max_length=255)
    id_card = models.FileField(upload_to='id_cards/', validators=[validate_file_type, validate_id_card_size], null=True, blank=True)

    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    # ✅ Add these methods inside the Teacher model
    def get_first_name(self):
        """Returns the first name of the teacher."""
        return self.name.split()[0] if self.name else ""

    def get_last_name(self):
        """Returns the last name(s) of the teacher."""
        parts = self.name.split()
        return " ".join(parts[1:]) if len(parts) > 1 else ""

    def __str__(self):
        return self.name

# Student Model
class Student(models.Model):
    student_id = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    branch = models.CharField(max_length=100)
    institute = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not is_password_usable(self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Idea Model
class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate Idea with a user
    college_name = models.CharField(max_length=255, default="SIES Graduate School of Technology")
    title = models.CharField(max_length=255)
    academic_year = models.CharField(max_length=10, default=get_current_academic_year)
    branch = models.CharField(max_length=100)
    domain = models.CharField(max_length=50)
    innovation_type = models.CharField(max_length=255)
    status_level = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])

    problem = models.TextField()
    solution = models.TextField()
    features = models.TextField()
    difference = models.TextField()
    video_url = models.URLField(blank=True, null=True)

    team_size = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    idea_description = models.TextField()
    project_stage = models.CharField(max_length=100)

    # ✅ PDF Upload - Max 200MB
    upload = models.FileField(upload_to='documents/', validators=[validate_file_type, validate_pdf_size], blank=True, null=True)

    mentor = models.CharField(max_length=255)
    develop_as_part = models.CharField(
    max_length=255,
    choices=[
        ("academic_requirement", "Academic Requirement/Study Project"),
        ("academic_research", "Academic Research Assignment/Industry Sponsored Project"),
        ("independent_assignment", "Independent Assignment/Non-academic Study Project")
    ],
    default="academic_requirement"  # Set a default value
)

    team_leader_name = models.CharField(max_length=100)
    team_leader_email = models.EmailField()
     # ✅ Team Leader ID Card - Max 2MB
    team_leader_id_card = models.FileField(upload_to='team_leader_id_cards/', validators=[validate_file_type, validate_id_card_size], blank=True, null=True)

    def __str__(self):
        return self.title
    
    def clean(self):
        """Ensure title is unique (case-insensitive)"""
        existing_idea = Idea.objects.filter(title__iexact=self.title).exclude(id=self.id)
        if existing_idea.exists():
            raise ValidationError("A project with this title already exists. Please choose a different name.")

    def save(self, *args, **kwargs):
        """Convert title to lowercase for case-insensitive uniqueness"""
        self.title = self.title.strip()  # Remove extra spaces
        super().save(*args, **kwargs)

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    id_card = models.FileField(upload_to='team_member_id_cards/', validators=[validate_file_type])
    project = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='team_members')

    def __str__(self):
        return self.name
    

class Prototype(models.Model):
    # Define the fields for the Prototype model
    #prototype_title = models.CharField(max_length=255)  # ✅ Add this
    from django.contrib.auth.hashers import make_password, is_password_usable
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

# Validator for file types
def validate_file_type(value):
    if not value.name.endswith(('.png', '.jpg', '.jpeg', '.pdf')):
        raise ValidationError(f"Invalid file type for {value.name}. Accepted formats: PNG, JPG, PDF.")

def validate_id_card_size(value):
    max_size = 2 * 1024 * 1024  # 2MB
    if value.size > max_size:
        raise ValidationError("ID Card file must be less than 2MB.")

# General PDF max size 200MB
def validate_pdf_size(value):
    max_size = 200 * 1024 * 1024  # 200MB
    if value.size > max_size:
        raise ValidationError("Uploaded PDF file must be less than 200MB.")

# Gender Choices
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

# Function to get academic year dynamically
def get_current_academic_year():
    current_year = datetime.now().year
    return f"{current_year}-{current_year + 1}"

# Teacher Model
class Teacher(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    branch = models.CharField(max_length=100)
    teacher_id = models.CharField(unique=True, max_length=50)
    institute = models.CharField(max_length=255)
    id_card = models.FileField(upload_to='id_cards/', validators=[validate_file_type, validate_id_card_size], null=True, blank=True)

    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    # ✅ Add these methods inside the Teacher model
    def get_first_name(self):
        """Returns the first name of the teacher."""
        return self.name.split()[0] if self.name else ""

    def get_last_name(self):
        """Returns the last name(s) of the teacher."""
        parts = self.name.split()
        return " ".join(parts[1:]) if len(parts) > 1 else ""

    def __str__(self):
        return self.name

# Student Model
class Student(models.Model):
    student_id = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    branch = models.CharField(max_length=100)
    institute = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not is_password_usable(self.password):  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Idea Model
class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow blank user for existing rows # Link Idea to the logged-in user
    college_name = models.CharField(max_length=255, default="SIES Graduate School of Technology")
    title = models.CharField(max_length=255)
    academic_year = models.CharField(max_length=10, default=get_current_academic_year)
    branch = models.CharField(max_length=100)
    domain = models.CharField(max_length=50)
    innovation_type = models.CharField(max_length=255)
    status_level = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])

    problem = models.TextField()
    solution = models.TextField()
    features = models.TextField()
    difference = models.TextField()
    video_url = models.URLField(blank=True, null=True)

    team_size = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    idea_description = models.TextField()
    project_stage = models.CharField(max_length=100)

    # ✅ PDF Upload - Max 200MB
    upload = models.FileField(upload_to='documents/', validators=[validate_file_type, validate_pdf_size], blank=True, null=True)

    mentor = models.CharField(max_length=255)
    develop_as_part = models.CharField(
    max_length=255,
    choices=[
        ("academic_requirement", "Academic Requirement/Study Project"),
        ("academic_research", "Academic Research Assignment/Industry Sponsored Project"),
        ("independent_assignment", "Independent Assignment/Non-academic Study Project")
    ],
    default="academic_requirement"  # Set a default value
)

    team_leader_name = models.CharField(max_length=100)
    team_leader_email = models.EmailField()
     # ✅ Team Leader ID Card - Max 2MB
    team_leader_id_card = models.FileField(upload_to='team_leader_id_cards/', validators=[validate_file_type, validate_id_card_size], blank=True, null=True)
    evaluated = models.BooleanField(default=False) 


    def __str__(self):
        return self.title
    
    def clean(self):
        """Ensure title is unique (case-insensitive)"""
        existing_idea = Idea.objects.filter(title__iexact=self.title).exclude(id=self.id)
        if existing_idea.exists():
            raise ValidationError("A project with this title already exists. Please choose a different name.")

    def save(self, *args, **kwargs):
        """Convert title to lowercase for case-insensitive uniqueness"""
        self.title = self.title.strip()  # Remove extra spaces
        super().save(*args, **kwargs)

    def get_type(self):
        return "Idea"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    id_card = models.FileField(upload_to='team_member_id_cards/', validators=[validate_file_type])
    project = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='team_members')

    def __str__(self):
        return self.name
    
class Prototype(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    prototype_title = models.CharField(max_length=255)
    description = models.TextField()
    college_name = models.CharField(max_length=255, default="SIES Graduate School of Technology")
    academic_year = models.CharField(max_length=10, default=get_current_academic_year)
    branch = models.CharField(max_length=100)
    domain = models.CharField(max_length=50)
    innovation_type = models.CharField(max_length=255)
    problem = models.TextField()
    solution = models.TextField()
    features = models.TextField()
    difference = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    team_size = models.PositiveIntegerField()
    status_level = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], default=1)
    prototype_files = models.FileField(upload_to="prototype_files/", blank=True, null=True)
    team_count = models.PositiveIntegerField(default=1)
    upload = models.FileField(upload_to='documents/', blank=True, null=True)
    mentor = models.CharField(max_length=255)
    develop_as_part = models.CharField(
        max_length=255,
        choices=[
            ("academic_requirement", "Academic Requirement/Study Project"),
            ("academic_research", "Academic Research Assignment/Industry Sponsored Project"),
            ("independent_assignment", "Independent Assignment/Non-academic Study Project")
        ],
        default="academic_requirement"
    )
    team_leader_name = models.CharField(max_length=100)
    team_leader_email = models.EmailField()
    team_leader_id_card = models.FileField(upload_to='team_leader_id_cards/', blank=True, null=True)
    evaluated = models.BooleanField(default=False)

    def __str__(self):
        return self.prototype_title

    def clean(self):
        existing_prototype = Prototype.objects.filter(prototype_title__iexact=self.prototype_title).exclude(id=self.id)
        if existing_prototype.exists():
            raise ValidationError("A prototype with this title already exists. Please choose a different name.")

    def save(self, *args, **kwargs):
        self.prototype_title = self.prototype_title.strip()
        super().save(*args, **kwargs)

    def get_type(self):
        return "Prototype"
    
        
class PrototypeTeamMember(models.Model):
    name = models.CharField(max_length=100)  # Add this field
    email = models.EmailField(unique=True)
    id_card = models.FileField(upload_to='team_member_id_cards/', blank=True, null=True)
    team_leader_name = models.CharField(max_length=255, blank=True, null=True)
    prototype = models.ForeignKey(Prototype, on_delete=models.CASCADE, related_name='prototype_team_members')

    def __str__(self):
        return self.name

# Startup Model
class Startup(models.Model):
    # Existing fields
    startup_name = models.CharField(max_length=255)  # Non-nullable (OK)
    title = models.CharField(max_length=20)  # Non-nullable (OK)
    website = models.URLField(blank=True, null=True)  # Nullable (OK)
    branch = models.CharField(
        max_length=100,
        null=True,  # Allow null temporarily
        blank=True  # Allow blank in forms temporarily
    )  # Nullable (OK)
    status_level = models.IntegerField(
        choices=[
            (1, 'Level 1'),
            (2, 'Level 2'),
            (3, 'Level 3')
        ],
        default=1  # Default value for status_level (OK)
    )
    registration = models.TextField(max_length=1000)  # Non-nullable (OK)
    key_innovation = models.TextField(max_length=1000)  # Non-nullable (OK)
    incubation_year = models.IntegerField()  # Non-nullable (OK)
    innovation_development = models.TextField(max_length=1000)  # Non-nullable (OK)
    sector = models.TextField(max_length=1000)  # Non-nullable (OK)
    innovation_type = models.CharField(max_length=50)  # Non-nullable (OK)
    video_url = models.URLField(null=True, blank=True)  # Non-nullable (OK)
    innovation_image = models.FileField(upload_to='innovation_images/', default='default_image.pdf')
    mentor = models.CharField(max_length=255)  # Non-nullable (OK)
    team_leader_name = models.CharField(max_length=255)  # Non-nullable (OK)
    team_leader_email = models.EmailField()  # Non-nullable (OK)
    team_leader_id_card = models.FileField(upload_to='id_cards/', null=True, blank=True)   
    team_count = models.IntegerField(default=0)  # Default value (OK)
    evaluated = models.BooleanField(default=False) 
    def __str__(self):
        return self.startup_name
    
    def get_type(self):
        return "Startup"
    
# Startup Team Member Model
class StartupTeamMember(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name="team_members")  # Link to the Startup model
    name = models.CharField(max_length=255,null=True, blank=True)  # Name of the team member
    email = models.EmailField()  # Email of the team member
    id_card = models.FileField(upload_to='startup_files/', blank=True, null=True)  # ID card file of the team member
    team_leader_name = models.CharField(max_length=255,null=True, blank=True)  # Name of the team leader

    def __str__(self):
        return f"Startup Team Member: {self.name} ({self.startup.startup_name})"
    
class PrototypeTeamMember(models.Model):
    prototype_title = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    id_card = models.FileField(upload_to='team_member_id_cards/', blank=True, null=True)  # New field
    team_leader_name = models.CharField(max_length=255, blank=True, null=True)  # New field
    prototype = models.ForeignKey(Prototype, on_delete=models.CASCADE, related_name='prototype_team_members')

    def __str__(self):
        return self.prototype_title
    

class Project(models.Model):
    teacher = models.ForeignKey('project_repo.Teacher', on_delete=models.CASCADE)  # String reference for Teacher
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='projects', default=1)  # Replace 1 with an appropriate default student ID
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    mentor = models.CharField(max_length=255, default='No Mentor')
    id_card_url = models.URLField(null=True, blank=True)  # Field

    def __str__(self):
        return self.name
    
class Evaluation(models.Model):
    project = models.ForeignKey('project_repo.Project', on_delete=models.CASCADE)
    score = models.IntegerField()
    feedback = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'  # Default value added here
    )
    def __str__(self):
        return f"Evaluation: {self.status} - {self.score}"
    
class StudentProject(models.Model):
    project_name = models.CharField(max_length=255)
    project_id = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=100)
    team_leader = models.CharField(max_length=255)
    mentor = models.CharField(max_length=255)

    def __str__(self):
        return self.project_name
    
class Evaluation(models.Model):
    project_name = models.CharField(max_length=200)
    team_leader_name = models.CharField(max_length=100)
    mentor_name = models.CharField(max_length=100)
    quality_of_problems = models.IntegerField()
    awareness_of_background = models.IntegerField()
    technique_justification = models.IntegerField()
    planning_scheduling = models.IntegerField()
    communication_clarity = models.IntegerField()
    total_marks = models.IntegerField()
    project_type = models.CharField(max_length=50)
    average = models.FloatField(null=True, blank=True)

    project_id = models.IntegerField()
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Safely cast values to integers
        q1 = int(self.quality_of_problems)
        q2 = int(self.awareness_of_background)
        q3 = int(self.technique_justification)
        q4 = int(self.planning_scheduling)
        q5 = int(self.communication_clarity)

        self.average = (q1 + q2 + q3 + q4 + q5) / 5.0
        self.total_marks = q1 + q2 + q3 + q4 + q5

        super(Evaluation, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_name} - {self.team_leader_name}"