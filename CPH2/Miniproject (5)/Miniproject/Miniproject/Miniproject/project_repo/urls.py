from django.urls import path
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from project_repo import views
from django.urls import reverse
from .views import reset_password,reset_password_view,evaluated_project
urlpatterns =  [

    # Redirect to login
    path('', lambda request: redirect('login/')),

    # Authentication routes
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', views.login_view, name='login'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-code/", views.verify_code, name="verify_code"),
    path("verify-email/", views.verify_email, name="verify_email"),
    path("reset-password/<uidb64>/<token>/", views.reset_password_view, name="reset_password"),
    path('choose-role/', views.choose_role, name='choose_role'),
    path('reset/<uidb64>/<token>/', views.reset_password_view, name='password_reset_confirm'),

    # Registration routes
    path('student_register/', views.register, name='register'),
    path('teacher-register/', views.teacher_register, name='teacher_register'),

    # Dashboard routes
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),

    # Projects routes
    path('projects/', views.projects, name='projects'),
    path('projects/', views.projects, name='project_page'),
    path('edit_project/<int:prototype_id>/', views.edit_prototype, name='edit_project'),  # Add this line

    # Idea-related routes
    path('idea_form/', views.idea_form, name='idea_form'),
    path('submit-idea/', views.submit_idea, name='submit_idea'),
    path('save_idea/', views.save_idea, name='save_idea'),
    path('idea_success/', views.idea_success, name='idea_success'),
    

    # Prototype-related routes
    path('prototype_form/', views.prototype_form, name='prototype_form'),
    path('submit_prototype/', views.submit_prototype, name='submit_prototype'),
    path('edit-prototype/<int:prototype_id>/', views.edit_prototype, name='edit_prototype'),

    # Startup-related routes
    path('start_up/', views.start_up, name='start_up'),
    path('submit-business/', views.submit_business, name='submit_business'),
    path('start_up/', views.start_up, name='start_up'),


    # Profile routes
    path('profile/', views.profile, name='profile_page'),
    path('student_profile/', views.student_profile, name='student_profile'),

    # Contact and About Us routes
    path('contact/', views.contact, name='contact_page'),
    path('about/', views.about_us, name='about_us'),

    # Validation routes
    path('validate_mobile/', views.validate_mobile, name='validate_mobile'),
    path('validate_prn/', views.validate_prn, name='validate_prn'),
    path('validate_teacher_id/', views.validate_teacher_id, name='validate_teacher_id'),

    # Dynamic project detail route

    path('project_details/<str:project_type>/<int:project_id>/', views.project_detail, name='project_detail'), 
   
    # Success page
    path('reset-password/', reset_password_view, name='reset_password'),
    path('reset_password/', reset_password_view, name='reset_password_view'),
    path('success/', views.success_page, name='success_page'),

    path('student-projects/', views.student_projects, name='student_projects'),


    
    path('teacher/evaluated/<str:project_type>/<int:project_id>/', views.evaluated_project, name='evaluated_project'),
    path('teacher/evaluated-projects/', views.teacher_evaluations, name='evaluated_projects'),  # <- Use the correct view
    path('teacher/evaluations/', views.teacher_evaluations, name='teacher_evaluations'),
    path('teacher/evaluations/<int:project_id>/', views.toggle_evaluation, name='toggle_evaluation'),
    path('evaluated_project/<str:project_type>/<int:project_id>/', views.evaluated_project, name='evaluated_project'),
    
    path('evaluation_details/<str:project_type>/<int:project_id>/', views.evaluation_details, name='evaluation_details'),    
    path('get-teachers/', views.get_teachers, name='get_teachers'),
    path('api/get_teachers/', views.get_teachers, name='get_teachers'),
 ]