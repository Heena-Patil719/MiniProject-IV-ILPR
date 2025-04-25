from django.contrib import admin
from django.utils.html import format_html
from .models import Student, Teacher, Idea, TeamMember, Prototype, PrototypeTeamMember,Evaluation
from .models import Startup, StartupTeamMember


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email', 'mobile', 'gender', 'branch', 'institute')
    search_fields = ('name', 'email', 'student_id', 'institute')
    list_filter = ('branch', 'gender', 'institute')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'branch', 'teacher_id', 'institute','id_card')
    search_fields = ('name', 'email', 'teacher_id')
    list_filter = ('branch', 'gender', 'institute')

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1  # Allows adding extra team members directly in the Idea admin panel
    fields = ('name', 'email', 'id_card')  # Added 'id_card' field
    readonly_fields = ('id_card',)  # Make ID card visible but not editable


#IDEA

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = (
        'develop_as_part', 'title', 'academic_year', 'branch', 'domain', 'innovation_type',
        'status_level', 'problem', 'solution', 'features', 'difference', 'video_url', 'upload',
        'mentor', 'team_leader_name', 'team_leader_email', 'team_leader_id_card', 'get_team_count'
    )
    search_fields = ('title', 'team_leader_name', 'team_leader_email', 'mentor', 'branch', 'domain')
    list_filter = ('academic_year', 'branch', 'domain', 'innovation_type', 'status_level')
    inlines = [TeamMemberInline]  # Allow managing team members in the same view

    def get_team_count(self, obj):
        return obj.team_members.count()  # Use 'team_members' instead of 'teammember_set'

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'project', 'id_card')  # Added 'id_card' field
    list_filter = ('project__academic_year', 'project__branch')



# Inline class for the PrototypeTeamMember model to display team members within the Prototype form
class PrototypeTeamMemberInline(admin.TabularInline):
    model = PrototypeTeamMember
    extra = 1  # Number of empty forms to display

@admin.register(Prototype)
class PrototypeAdmin(admin.ModelAdmin):
    list_display = ('prototype_title', 'academic_year', 'branch', 'domain', 'innovation_type', 
                    'problem', 'solution', 'features', 'difference', 'video_url', 'team_size', 
                    'upload', 'mentor', 'develop_as_part', 'team_leader_name', 'team_leader_email', 'team_leader_id_card')
    search_fields = ('prototype_title', 'academic_year', 'branch', 'domain', 'mentor')
    list_filter = ('academic_year', 'branch', 'innovation_type', 'develop_as_part')

    fieldsets = (
        (None, {
            'fields': ('prototype_title', 'academic_year', 'branch', 'domain', 'innovation_type')
        }),
        ('Project Details', {
            'fields': ('problem', 'solution', 'features', 'difference', 'video_url', 'team_size', 
                       'upload')
        }),
        ('Mentor & Development', {
            'fields': ('mentor', 'develop_as_part')
        }),
        ('Team Details', {
            'fields': ('team_leader_name', 'team_leader_email', 'team_leader_id_card')
        }),
    )
@admin.register(PrototypeTeamMember)
class PrototypeTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('prototype_title', 'email', 'prototype', 'id_card', 'team_leader_name')  # Include 'team_leader_name' in the list_display
    search_fields = ('prototype_title', 'email')
    list_filter = ('prototype',)

    fieldsets = (
        (None, {
            'fields': ('prototype_title', 'email', 'id_card')
        }),
        ('Prototype Details', {
            'fields': ('prototype', 'team_leader_name')
        }),
    )

    def team_leader_name(self, obj):
        return obj.prototype.team_leader_name  # Access 'team_leader_name' from the related Prototype instance
    team_leader_name.short_description = 'Team Leader Name'  # Set the name that will appear in the Admin panel


class StartupTeamMemberInline(admin.TabularInline):
    model = StartupTeamMember
    extra = 1  # Allows adding extra team members directly in the Startup admin page

class StartupAdmin(admin.ModelAdmin):
    list_display = (
        'startup_name', 'title', 'website', 'registration', 'key_innovation', 
        'incubation_year', 'innovation_development', 'sector', 'innovation_type', 
        'video_url', 'innovation_image', 'mentor', 'team_leader_name', 'team_leader_email', 
        'team_leader_id_card'
    )
    search_fields = ('startup_name', 'title', 'mentor', 'team_leader_name')
    list_filter = ('innovation_type', 'incubation_year')
    inlines = [StartupTeamMemberInline]  # Show team members inside Startup admin

class StartupTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'startup')
    search_fields = ('name', 'email')
    list_filter = ('startup',)

admin.site.register(Startup, StartupAdmin)
admin.site.register(StartupTeamMember, StartupTeamMemberAdmin)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'project_name', 'team_leader_name', 'mentor_name',
        'total_marks', 'average', 'project_type',
    )
    search_fields = ('project_name', 'team_leader_name', 'mentor_name')
