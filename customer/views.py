import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse

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


''' 
    TODO 
    - Create a decorator to verify that a user is logged in and they have subscribed to the course
    - We can name it @is_subscribed
'''
@login_required
def course_lesson_session(request, course_id):
    course = selectors.get_specific_course(course_id)
    first_section = course.sections.order_by('id').first()
    lesson = first_section.lessons.order_by('id').first()

    # if request.method == "POST":
    #     lesson_id = request.POST.get("lesson-id")
    #     return redirect(f"customer/learning/{course.id}/{lesson_id}")

    context = {
        "lesson": lesson,
        "course": course
    }
    

    return render(request, "dashboard/customer/student_course_session.html", context)


@login_required
def course_lesson_specific_session(request, course_id, lesson_id):
    course = selectors.get_specific_course(course_id)
    lesson = selectors.get_specific_lesson(lesson_id)

    context = {
        "lesson": lesson,
        "course": course
    }

    return render(request, "dashboard/customer/student_course_session.html", context)
