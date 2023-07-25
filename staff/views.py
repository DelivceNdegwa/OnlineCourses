from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required

from courses import selectors
from staff import forms
# Create your views here.
'''
    The home view contains: A table of current courses subscribed by students, courses generally, notifications, categories 
'''
@staff_member_required
def home(request):
    context = {
        "categories": selectors.get_categories(),
        "courses": selectors.get_courses(),
        "enrolled_courses": selectors.get_courses_with_active_students()
    }
    return render(request, "dashboard/admin/home.html", context)

@staff_member_required
def categories(request):
    paginator = Paginator(selectors.get_categories(), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = forms.CategoryForm()
    if request.method == "POST":
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("staff:categories")
    context = {
        "page_obj": page_obj,
        "form": form,
        "modal_title": "Category creation"
    }
    return render(request, "dashboard/admin/categories.html", context)

@staff_member_required
def courses(request):
    context = {
        "categories": selectors.get_courses()
    }
    return render(request, "dashboard/admin/courses.html", context)