from django.contrib import admin
from .models import Department, Student, Course, Enrollment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'department', 'cgpa')
    list_filter = ('department', 'gender', 'admission_date')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'title', 'department', 'credit_hours')
    list_filter = ('department', 'credit_hours')
    search_fields = ('course_code', 'title')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'year', 'grade')
    list_filter = ('semester', 'year', 'grade')
    search_fields = ('student__student_id', 'student__first_name', 'student__last_name', 'course__course_code')
