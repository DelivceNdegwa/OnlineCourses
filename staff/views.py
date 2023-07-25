from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

from courses import selectors, services
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
    categories = selectors.get_categories()
    paginator = Paginator(categories, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = forms.CategoryForm()
    if request.method == "POST":
        form = forms.CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("staff:categories")
    context = {
        "categories": categories,
        "page_obj": page_obj,
        "form": form,
        "modal_title": "Category"
    }
    return render(request, "dashboard/admin/categories.html", context)

@staff_member_required
def read_update_category(request, category_id):
    category = selectors.get_specific_category(category_id)
    form = forms.CategoryForm(instance=category)
    message = ""
    success = False
    
    if request.method == "POST":
        form = forms.CategoryForm(request.POST, request.FILES, instance=category)   
        if form.is_valid():
            form.save()
            success = True
            message = f"Category {category.name} has been updated"
            url = reverse('staff:read_update_category', kwargs={'category_id': category_id})
            return redirect(url)
        else:
            message = f"Could not update {category.name}"
    context = {
        "message": message,
        "success": success,
        "category": category,
        "form": form
    }
    return render(request, "dashboard/admin/specific_category.html", context)

@staff_member_required
def delete_category(request, category_id):
    error = ""

    try:
        services.delete_category(category_id)
        return redirect("staff:categories")
    except Exception as e:
        error = "Something went wrong: {e}"

    context = {
        "error": error
    }

    return render(request, "dashboard/admin/specific_category.html", context)

@staff_member_required
def courses(request):
    courses = selectors.get_courses()
    paginator = Paginator(courses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = forms.CourseForm()

    if request.method == "POST":
        form = forms.CourseForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("staff:courses")
    
    context = {
        "courses": courses,
        "page_obj": page_obj,
        "form": form,
        "modal_title": "Course"
    }
    
    return render(request, "dashboard/admin/courses.html", context)
