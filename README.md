# Student Enrollment Analysis System (SEAS)

A web-based application written in Python (Django) to analyze the enrollment data of university students, particularly students from Independent University.

## Features

- Dashboard with key metrics and visualizations
- Department management
- Student management
- Course management
- Enrollment tracking
- Data analysis and reporting
- Responsive design using Bootstrap

## Technology Stack

- **Backend**: Django 5.2.1
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **Charts**: Chart.js

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/seas.git
   cd seas
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Load sample data (optional):
   ```
   python manage.py create_sample_data
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Usage

### Admin Interface

Access the admin interface at http://127.0.0.1:8000/admin/ using your superuser credentials.

### Dashboard

The dashboard provides an overview of key metrics:
- Total students
- Total courses
- Total departments
- Total enrollments
- Department-wise student count
- Recent enrollments

### Data Analysis

The system provides various analysis options:
- Department-wise enrollment analysis
- Course popularity analysis
- Semester-wise enrollment trends
- Year-wise enrollment trends
- Gender-wise enrollment distribution

## Project Structure

```
seas/
├── enrollment/              # Main application
│   ├── management/          # Custom management commands
│   ├── migrations/          # Database migrations
│   ├── templatetags/        # Custom template tags
│   ├── admin.py             # Admin interface configuration
│   ├── forms.py             # Form definitions
│   ├── models.py            # Data models
│   ├── urls.py              # URL routing
│   └── views.py             # View functions
├── seas/                    # Project settings
├── static/                  # Static files (CSS, JS)
├── templates/               # HTML templates
├── manage.py                # Django management script
└── README.md                # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Django
- Bootstrap
- Chart.js
- Font Awesome