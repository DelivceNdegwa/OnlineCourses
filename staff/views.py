from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from courses import selectors

# Create your views here.
'''
    The home view contains: A table of current courses subscribed by students, courses generally, notifications, categories 
'''
@staff_member_required
def home(request):
    context = {
        "categories": selectors.get_categories(),
        "courses": selectors.get_courses()
    }
    return render(request, "dashboard/admin/home.html", context)

@staff_member_required
def categories(request):
    context = {
        "categories": selectors.get_categories()
    }
    return render(request, "dashboard/admin/categories.html", context)