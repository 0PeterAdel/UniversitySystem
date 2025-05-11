from django import forms
from .models import Department, Student, Course, Enrollment

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 
                 'gender', 'department', 'admission_date', 'cgpa']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'title', 'description', 'credit_hours', 'department']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'semester', 'year', 'grade', 'enrollment_date']
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EnrollmentAnalysisForm(forms.Form):
    ANALYSIS_CHOICES = [
        ('department', 'Department-wise Enrollment'),
        ('course', 'Course-wise Enrollment'),
        ('semester', 'Semester-wise Enrollment'),
        ('year', 'Year-wise Enrollment'),
        ('gender', 'Gender-wise Enrollment'),
    ]
    
    analysis_type = forms.ChoiceField(choices=ANALYSIS_CHOICES)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)