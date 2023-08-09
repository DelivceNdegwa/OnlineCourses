from django.shortcuts import render
from courses import selectors

def index(request):
    
    categories = selectors.get_categories()
    courses = selectors.get_courses()
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
