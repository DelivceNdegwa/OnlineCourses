from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required

from courses import selectors, services
from courses.models import Video
from courses.tasks import generate_dash_files
from staff import forms



def video_stream(request, video_id):
    # video = get_object_or_404(Video, pk=video_id)
    # dash_manifest_url = video.generate_dash()
    video = selectors.get_specific_video({'id': video_id})
    dash_manifest_url = video.dash_manifest

    return render(request, 'courses/video.html', {'dash_manifest_url': dash_manifest_url})


def test_stream(request):
    lesson_6 = selectors.get_specific_lesson(6)
    dash_manifest_url = lesson_6.video.dash_manifest

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
    course_form = forms.CourseForm(instance=course)
    message = ""
    success = False
    course_sections = selectors.get_course_sections(course_id)
    paginator = Paginator(course_sections, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
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
        "sections": page_obj,
        "form": form,
        "course_form": course_form,
        "message": message,
        "success": success
    }
    
    return render(request, "dashboard/admin/course_details.html", context)


@staff_member_required
def admin_edit_course_details(request, course_id):
    course = selectors.get_specific_course(course_id)
    form = forms.CourseForm(instance=course)
    
    if request.method == "POST":
        form = forms.CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
    url = reverse('staff:course_details', kwargs={'course_id': course_id})
    return redirect(url)

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


@staff_member_required
def admin_course_section_details(request, course_id, section_id):
    section = selectors.get_specific_section(section_id)
    section_items = selectors.get_lessons({"section__id": section_id})
    paginator = Paginator(section_items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = forms.SectionForm(instance=section)
    
    if request.method == "POST":
        title = request.POST.get("title")
        media_choice = request.POST.get("section_media_radio")
        print(f"REQUEST POST= {request.POST} {request.FILES}")
        
        if media_choice == "video":
            video_file = request.FILES.get("video_file")
            video = services.create_lesson_video(video_file)

            print(f"VIDEO={video.id}")

            services.create_section_item(
                title=title,
                section_id=section.id,
                video_id=video.id
            )
            # TODO: Create a background task for this
            # video.generate_dash()
            generate_dash_files.delay(video.id)
            return JsonResponse(data={"message": "Video is being processed", "success": True})
            
        if media_choice == "document":
            document_file = request.FILES.get("document_file")
            
            document = services.create_lesson_document(document_file)
            print(f"HERE IS DOC={document}:{document.id}")
            services.create_section_item(
                title=title,
                section_id=section.id,
                document_id=document.id
            )

        url = reverse("staff:admin_course_section_details", kwargs={"course_id": section.course.id, "section_id": section.id})
        return redirect(url)
    
    context = {
        "section": section,
        "section_items": page_obj,
        "total_lessons": section_items,
        "section_form": form
    }
    
    return render(request, "dashboard/admin/section_details.html", context)


@staff_member_required
def admin_course_section_details_update(request, course_id, section_id):
    section = selectors.get_specific_section(section_id)
    
    if request.method == "POST":
        form = forms.SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
    url = reverse("staff:admin_course_section_details", kwargs={"course_id": course_id, "section_id": section_id})
    return redirect(url)


@staff_member_required
def admin_course_section_lesson_details(request, course_id, section_id, lesson_id):
    lesson = selectors.get_specific_lesson(lesson_id)
    
    if request.method == "POST":
        video_file = None#request.FILES.get("video_file")
        document_file = None#request.FILES.get("document_file")
        video_changed = request.POST.get("video-changed")
        document_changed = request.POST.get("document-changed")
        print("--HERE GOES--")
        print(f"CHANGES {video_changed}, {document_changed}")
        title = request.POST.get("title")
        
        if video_changed == 'on' and video_file and lesson.video:
            video = selectors.get_specific_video({'id': lesson.video.id})
            if video.video_file is not video_file:
                video.video_file = video_file
                video.save()

        if document_changed == 'on' and document_file and lesson.document:
            document = selectors.get_specific_document({'id': lesson.document.id})
            if document.document_file is not document_file:
                document.document_file = document_file
                document.save()
        
        if title is not lesson.title:
            lesson.title=title
            lesson.save()
            
    context = {
        "lesson": lesson,
        "section": lesson.section
    }   
    
    return render(request, "dashboard/admin/lesson_details.html", context)

