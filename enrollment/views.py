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
import csv
from datetime import datetime
from django.http import HttpResponse

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
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(student_id__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(department__name__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

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
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(course_code__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(department__name__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

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
def analysis_dashboard(request):
    # Get counts
    department_count = Department.objects.count()
    student_count = Student.objects.count()
    course_count = Course.objects.count()
    enrollment_count = Enrollment.objects.count()
    
    # Get departments with stats
    departments = Department.objects.annotate(
        student_count=Count('students', distinct=True),
        course_count=Count('courses', distinct=True),
        enrollment_count=Count('students__enrollments', distinct=True)
    )
    
    # Get top courses by enrollment
    top_courses = Course.objects.annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-enrollment_count')[:5]
    
    # Get recent enrollments
    recent_enrollments = Enrollment.objects.select_related(
        'student', 'course', 'course__department'
    ).order_by('-enrollment_date')[:10]
    
    context = {
        'department_count': department_count,
        'student_count': student_count,
        'course_count': course_count,
        'enrollment_count': enrollment_count,
        'departments': departments,
        'top_courses': top_courses,
        'recent_enrollments': recent_enrollments,
    }
    
    return render(request, 'enrollment/analysis_dashboard.html', context)

def department_analysis(request):
    # Get departments with stats
    departments = Department.objects.annotate(
        student_count=Count('students', distinct=True),
        course_count=Count('courses', distinct=True),
        enrollment_count=Count('students__enrollments', distinct=True),
        avg_cgpa=Avg('students__cgpa')
    )
    
    context = {
        'departments': departments,
    }
    
    return render(request, 'enrollment/department_analysis.html', context)

def course_analysis(request):
    # Get all courses with stats
    courses = Course.objects.annotate(
        enrollment_count=Count('enrollments')
    ).select_related('department').order_by('-enrollment_count')
    
    # Get top courses by enrollment
    top_courses = courses[:10]
    
    # Calculate grade distribution
    grade_distribution = {
        'A': Enrollment.objects.filter(grade='A').count(),
        'A_minus': Enrollment.objects.filter(grade='A-').count(),
        'B_plus': Enrollment.objects.filter(grade='B+').count(),
        'B': Enrollment.objects.filter(grade='B').count(),
        'B_minus': Enrollment.objects.filter(grade='B-').count(),
        'C_plus': Enrollment.objects.filter(grade='C+').count(),
        'C': Enrollment.objects.filter(grade='C').count(),
        'C_minus': Enrollment.objects.filter(grade='C-').count(),
        'D_plus': Enrollment.objects.filter(grade='D+').count(),
        'D': Enrollment.objects.filter(grade='D').count(),
        'F': Enrollment.objects.filter(grade='F').count(),
        'W': Enrollment.objects.filter(grade='W').count(),
        'I': Enrollment.objects.filter(grade='I').count(),
    }
    
    context = {
        'courses': courses,
        'top_courses': top_courses,
        'grade_distribution': grade_distribution,
    }
    
    return render(request, 'enrollment/course_analysis.html', context)

@login_required
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    # Get query parameters for filtering
    search_query = request.GET.get('search', '')
    
    # Get students with optional filtering
    students = Student.objects.all()
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) | 
            Q(student_id__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )
    
    # Create CSV writer
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Name', 'Email', 'Department', 'Gender', 'Date of Birth', 'CGPA'])
    
    # Add student data
    for student in students:
        writer.writerow([
            student.student_id,
            student.full_name,
            student.email,
            student.department.name if student.department else 'N/A',
            student.get_gender_display(),
            student.date_of_birth.strftime('%Y-%m-%d') if student.date_of_birth else 'N/A',
            student.cgpa
        ])
    
    return response

def student_analysis(request):
    # Get top students by CGPA
    top_students = Student.objects.annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-cgpa')[:20]
    
    # Get departments with stats
    departments = Department.objects.annotate(
        student_count=Count('students', distinct=True),
        avg_cgpa=Avg('students__cgpa')
    )
    
    # Calculate CGPA distribution
    cgpa_distribution = {
        'range_0_0_5': Student.objects.filter(cgpa__gte=0, cgpa__lt=0.5).count(),
        'range_0_5_1_0': Student.objects.filter(cgpa__gte=0.5, cgpa__lt=1.0).count(),
        'range_1_0_1_5': Student.objects.filter(cgpa__gte=1.0, cgpa__lt=1.5).count(),
        'range_1_5_2_0': Student.objects.filter(cgpa__gte=1.5, cgpa__lt=2.0).count(),
        'range_2_0_2_5': Student.objects.filter(cgpa__gte=2.0, cgpa__lt=2.5).count(),
        'range_2_5_3_0': Student.objects.filter(cgpa__gte=2.5, cgpa__lt=3.0).count(),
        'range_3_0_3_5': Student.objects.filter(cgpa__gte=3.0, cgpa__lt=3.5).count(),
        'range_3_5_4_0': Student.objects.filter(cgpa__gte=3.5, cgpa__lte=4.0).count(),
    }
    
    context = {
        'top_students': top_students,
        'departments': departments,
        'cgpa_distribution': cgpa_distribution,
    }
    
    return render(request, 'enrollment/student_analysis.html', context)

@login_required
def enrollment_analysis(request):
    form = EnrollmentAnalysisForm(request.GET or None)
    
    # Get enrollment counts
    enrollment_count = Enrollment.objects.count()
    student_count = Student.objects.count()
    course_count = Course.objects.count()
    
    # Calculate averages
    avg_enrollments_per_student = enrollment_count / student_count if student_count > 0 else 0
    avg_enrollments_per_course = enrollment_count / course_count if course_count > 0 else 0
    
    # Get departments with enrollment counts
    departments = Department.objects.annotate(
        enrollment_count=Count('students__enrollments', distinct=True)
    )
    
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
        'analysis_data': json.dumps(analysis_data),
        'enrollment_count': enrollment_count,
        'avg_enrollments_per_student': avg_enrollments_per_student,
        'avg_enrollments_per_course': avg_enrollments_per_course,
        'avg_grade': 'B+',  # Placeholder, calculate actual average grade if needed
        'departments': departments,
    }
    
    return render(request, 'enrollment/enrollment_analysis.html', context)

@login_required
def student_performance(request):
    departments = Department.objects.all()
    department_id = request.GET.get('department')
    sort_by = request.GET.get('sort_by', 'cgpa')  # Default sort by CGPA
    
    students = []
    if department_id:
        students = Student.objects.filter(department_id=department_id)
        
        # Apply sorting
        if sort_by == 'cgpa':
            students = students.order_by('-cgpa')
        elif sort_by == 'enrollments':
            students = students.annotate(enrollment_count=Count('enrollments')).order_by('-enrollment_count')
        elif sort_by == 'name':
            students = students.order_by('name')
        elif sort_by == 'id':
            students = students.order_by('student_id')
        
        # Get performance metrics
        total_students = students.count()
        avg_cgpa = students.aggregate(Avg('cgpa'))['cgpa__avg'] or 0
        
        # Get grade distribution for this department
        grade_distribution = {}
        for grade_code, grade_name in Enrollment.GRADE_CHOICES:
            count = Enrollment.objects.filter(student__department_id=department_id, grade=grade_code).count()
            grade_distribution[grade_name] = count
    else:
        total_students = 0
        avg_cgpa = 0
        grade_distribution = {}
    
    context = {
        'departments': departments,
        'students': students,
        'selected_department': department_id,
        'sort_by': sort_by,
        'total_students': total_students,
        'avg_cgpa': avg_cgpa,
        'grade_distribution': grade_distribution
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
