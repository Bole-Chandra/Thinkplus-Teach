from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Assignment, Submission

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['created_at']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'plagiarism_score', 'grade', 'is_evaluated', 'submitted_at']
    list_filter = ['is_evaluated', 'submitted_at']
    search_fields = ['student__username', 'assignment__title']
    readonly_fields = ['plagiarism_score', 'feedback', 'is_evaluated']

admin.site.register(User, CustomUserAdmin)
