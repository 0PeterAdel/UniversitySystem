from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count, Avg, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from .models import Department, Student, Course, Enrollment
from .forms import DepartmentForm, StudentForm, CourseForm, EnrollmentForm, EnrollmentAnalysisForm

import json
from datetime import datetime

def home(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_departments = Department.objects.count()
    total_enrollments = Enrollment.objects.count()
    
    # Recent enrollments
    recent_enrollments = Enrollment.objects.order_by('-enrollment_date')[:5]
    
    # Department-wise student count
    dept_student_count = Department.objects.annotate(student_count=Count('students'))
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_departments': total_departments,
        'total_enrollments': total_enrollments,
        'recent_enrollments': recent_enrollments,
        'dept_student_count': dept_student_count,
    }
    
    return render(request, 'enrollment/home.html', context)

# Department Views
class DepartmentListView(ListView):
    model = Department
    template_name = 'enrollment/department_list.html'
    context_object_name = 'departments'

class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'enrollment/department_detail.html'
    context_object_name = 'department'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        context['students'] = Student.objects.filter(department=department)
        context['courses'] = Course.objects.filter(department=department)
        return context

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'enrollment/department_form.html'
    success_url = reverse_lazy('department-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Department created successfully!')
        return super().form_valid(form)

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'enrollment/department_form.html'
    success_url = reverse_lazy('department-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Department updated successfully!')
        return super().form_valid(form)

class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'enrollment/department_confirm_delete.html'
    success_url = reverse_lazy('department-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Department deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Student Views
class StudentListView(ListView):
    model = Student
    template_name = 'enrollment/student_list.html'
    context_object_name = 'students'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'enrollment/student_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context['enrollments'] = Enrollment.objects.filter(student=student)
        return context

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'enrollment/student_form.html'
    success_url = reverse_lazy('student-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Student created successfully!')
        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'enrollment/student_form.html'
    success_url = reverse_lazy('student-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Student updated successfully!')
        return super().form_valid(form)

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'enrollment/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Student deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Course Views
class CourseListView(ListView):
    model = Course
    template_name = 'enrollment/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'enrollment/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['enrollments'] = Enrollment.objects.filter(course=course)
        return context

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'enrollment/course_form.html'
    success_url = reverse_lazy('course-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'enrollment/course_form.html'
    success_url = reverse_lazy('course-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'enrollment/course_confirm_delete.html'
    success_url = reverse_lazy('course-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Course deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Enrollment Views
class EnrollmentListView(ListView):
    model = Enrollment
    template_name = 'enrollment/enrollment_list.html'
    context_object_name = 'enrollments'

class EnrollmentDetailView(DetailView):
    model = Enrollment
    template_name = 'enrollment/enrollment_detail.html'
    context_object_name = 'enrollment'

class EnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'enrollment/enrollment_form.html'
    success_url = reverse_lazy('enrollment-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Enrollment created successfully!')
        return super().form_valid(form)

class EnrollmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'enrollment/enrollment_form.html'
    success_url = reverse_lazy('enrollment-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Enrollment updated successfully!')
        return super().form_valid(form)

class EnrollmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'enrollment/enrollment_confirm_delete.html'
    success_url = reverse_lazy('enrollment-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Enrollment deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Analysis Views
@login_required
def enrollment_analysis(request):
    form = EnrollmentAnalysisForm(request.GET or None)
    
    analysis_data = {}
    labels = []
    data = []
    
    if form.is_valid():
        analysis_type = form.cleaned_data.get('analysis_type')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        department = form.cleaned_data.get('department')
        
        # Base queryset
        enrollments = Enrollment.objects.all()
        
        # Apply filters
        if start_date:
            enrollments = enrollments.filter(enrollment_date__gte=start_date)
        if end_date:
            enrollments = enrollments.filter(enrollment_date__lte=end_date)
        if department:
            enrollments = enrollments.filter(Q(student__department=department) | Q(course__department=department))
        
        # Perform analysis based on type
        if analysis_type == 'department':
            departments = Department.objects.all()
            for dept in departments:
                count = enrollments.filter(student__department=dept).count()
                labels.append(dept.name)
                data.append(count)
            chart_title = 'Department-wise Enrollment'
            
        elif analysis_type == 'course':
            courses = Course.objects.all()[:10]  # Limit to top 10 courses
            for course in courses:
                count = enrollments.filter(course=course).count()
                labels.append(course.course_code)
                data.append(count)
            chart_title = 'Course-wise Enrollment'
            
        elif analysis_type == 'semester':
            semesters = Enrollment.SEMESTER_CHOICES
            for semester_code, semester_name in semesters:
                count = enrollments.filter(semester=semester_code).count()
                labels.append(semester_name)
                data.append(count)
            chart_title = 'Semester-wise Enrollment'
            
        elif analysis_type == 'year':
            years = enrollments.values_list('year', flat=True).distinct().order_by('year')
            for year in years:
                count = enrollments.filter(year=year).count()
                labels.append(str(year))
                data.append(count)
            chart_title = 'Year-wise Enrollment'
            
        elif analysis_type == 'gender':
            genders = Student.GENDER_CHOICES
            for gender_code, gender_name in genders:
                count = enrollments.filter(student__gender=gender_code).count()
                labels.append(gender_name)
                data.append(count)
            chart_title = 'Gender-wise Enrollment'
        
        analysis_data = {
            'labels': labels,
            'data': data,
            'chart_title': chart_title
        }
    
    context = {
        'form': form,
        'analysis_data': json.dumps(analysis_data)
    }
    
    return render(request, 'enrollment/enrollment_analysis.html', context)

@login_required
def student_performance(request):
    departments = Department.objects.all()
    department_id = request.GET.get('department')
    
    students = []
    if department_id:
        students = Student.objects.filter(department_id=department_id).order_by('-cgpa')
    
    context = {
        'departments': departments,
        'students': students,
        'selected_department': department_id
    }
    
    return render(request, 'enrollment/student_performance.html', context)

@login_required
def course_popularity(request):
    courses = Course.objects.annotate(enrollment_count=Count('enrollments')).order_by('-enrollment_count')[:10]
    
    labels = [course.course_code for course in courses]
    data = [course.enrollment_count for course in courses]
    
    context = {
        'courses': courses,
        'chart_data': json.dumps({
            'labels': labels,
            'data': data
        })
    }
    
    return render(request, 'enrollment/course_popularity.html', context)
