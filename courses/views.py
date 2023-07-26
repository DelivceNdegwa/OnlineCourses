from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required

from courses import selectors, services
from courses.models import Video
from staff import forms



def video_stream(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    dash_manifest_url = video.generate_dash()

    return render(request, 'courses/video.html', {'dash_manifest_url': dash_manifest_url})


@staff_member_required
def admin_courses(request):
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


@staff_member_required
def admin_course_details(request, course_id):
    form = forms.SectionForm()
    course = selectors.get_specific_course(course_id)
    filter_by_course_id = {
        "course__id": course_id
    }
    message = ""
    success = False
    course_sections = selectors.get_course_sections(filter_by_course_id, extra_fields=['course__id'])
    
    if request.method == "POST":
        form = forms.SectionForm(request.POST)
        message = "Section was not created, something went wrong, please try again"

        if form.is_valid():
            title = form.cleaned_data["title"]
            try:
                services.create_section(title, course_id)
                message = "Section created successfully"
                success = True
                form = forms.SectionForm()
                url = reverse('staff:course_details', kwargs={'course_id': course_id})
                return redirect(url)
            except Exception as e:
                print(f"SECTION_CREATION: {e}")
            
    
    context = {
        "course": course,
        "sections": course_sections,
        "form": form,
        "message": message,
        "success": success
    }
    
    return render(request, "dashboard/admin/course_details.html", context)


@staff_member_required
def add_section(request, course_id):
    if request.method == "POST":
        form = forms.SectionForm(request.POST)
        message = ""
        status_code = 400
        success = False

        if form.is_valid():
            title = form.cleaned_data["title"]
            try:
                services.create_section(title, course_id)
                message = "Section created successfully"
                status_code = 200
                success = True
            except Exception as e:
                message = "Section was not created, something went wrong, please try again"
                print(f"SECTION_CREATION: {e}")
            
            response_data = {
                "message": message,
                "success": success
            }
            
            return JsonResponse(data=response_data, status_code=status_code)
    return JsonResponse(data="Only POST requests are allowed", status_code=400)


# @staff_member_required
# def section_details(request, course_id, section_id):
    
