from django.shortcuts import render
from courses import selectors

def index(request):
    
    categories = selectors.get_categories()
    courses = selectors.get_courses({'ready': True})
    context = {
        "categories": categories,
        "courses": courses
    }
    
    return render(request, "frontend/index.html", context)

def categories(request):
    categories = selectors.get_categories()

    context = {
        "categories": categories
    }

    return render(request, "frontend/categories.html", context)


def category_details(request, category_id):
    category = selectors.get_specific_category(category_id)
    category_courses = selectors.get_category_courses(category.id)

    context = {
        "category": category,
        "category_courses": category_courses
    }

    return render(request, "frontend/category_details.html", context)

def course_details(request, category_id,course_id):
    course = selectors.get_specific_course(course_id)

    context = {
        "course": course,
    }
    return render(request, "frontend/course_details.html", context)

    