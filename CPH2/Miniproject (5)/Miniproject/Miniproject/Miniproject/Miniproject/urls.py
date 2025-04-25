from django.contrib import admin
from django.urls import path, include 
from django.contrib.auth import views as auth_views  
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project_repo.urls')),  # Includes URLs from project_repo
      # Ensures captcha URLs are included

    # Password reset views
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete"),
]
# Add this to serve media files during development
if settings.DEBUG:  # Only include this in DEBUG mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)