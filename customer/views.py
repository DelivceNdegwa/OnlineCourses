from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from courses.models import (
    Category,
    Course,
    Subscription
)

from courses import selectors, services

User = get_user_model()


@login_required
def home(request):
    
    pending_stats_dict = {
        'type': 'pending',
        'count': 0,
        'description': 'Courses <br> pending'
    }
    completed_stats_dict = {
        'type': 'completed',
        'count': 0,
        'description': 'Courses <br> completed'
    }
    
    courses_stats_list = [pending_stats_dict, completed_stats_dict]
    
    context = {
        "courses_stats": courses_stats_list
    }
    return render(request, "dashboard/customer/home.html", context)

@login_required
def student_learning(request):
    student_filter = {
        "student__id": request.user.id,
    }
    subscriptions = selectors.get_all_subscriptions()
    student_courses = selectors.get_student_courses(student_filter, ["student_id"])
    context = {
        "subscriptions": student_courses
    }
    return render(request, "dashboard/customer/my_learning.html", context)
