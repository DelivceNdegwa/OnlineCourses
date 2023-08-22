from django.db import transaction

from courses.models import SystemSettings, Category, Section, VideoDocument, Video, Document, Subscription
from courses import selectors
from base import exceptions


# Create System Setting
@transaction.atomic
def create_system_setting(one_time_fee, monthly_fee) -> SystemSettings:
    setting = SystemSettings.objects.create(
                one_time_fee=one_time_fee,
                monthly_fee=monthly_fee
            )
    return setting


@transaction.atomic
def create_category(name, image, short_description) -> Category:
    category = Category.objects.create(
        name=name,
        image=image,
        short_description=short_description
    )
    return category


@transaction.atomic
def delete_category(category_id: int):
    category = selectors.get_specific_category(category_id)
    category.delete()
    return category


@transaction.atomic
def create_section(title, course_id):
    course = selectors.get_specific_course(course_id)
    filter_params = {
        "course__id": course.id,
        "title": title
    }

    section = selectors.get_course_sections(filter_params, ['course__id'])

    if section:
        print(f"--DUPLICATE-- ID->{course.title}:ID={section.first().course.title}, {section.first().title}")
        return section[0]
    
    section = Section.objects.create(
        title=title,
        course=course
    )
    return section


@transaction.atomic
def create_section_item(
    *,
    title: str,
    section_id: int,
    video_id: int = None,
    document_id: int = None,
    # position: int = None
):
    if not video_id and not document_id:
        raise exceptions.CustomException("Please provide a video or a document")
    
    video = selectors.get_specific_video({'id': video_id})
    document = selectors.get_specific_document({'id': document_id})
    section = selectors.get_specific_section(section_id)
    
    filter_params = {
        "title": title,
        "section__id": section_id,
        "video__id": video_id,
        "document__id": document_id
    }
    
    existing_item = selectors.get_lessons(filter_params, ["video__id", "document__id"])
    if not existing_item:
        video_doc = VideoDocument.objects.create(
            title=title,
            section=section,
            video=video,
            document=document
        )
        return video_doc
    return existing_item.first()

@transaction.atomic
def create_lesson_video(video):
    # exists = Video.objects.filter(video_file=video)
    # if not exists:
    #     return Video.objects.create(video_file=video)
    # return exists
    return Video.objects.create(video_file=video)

@transaction.atomic
def create_lesson_document(document):
    # exists = Document.objects.filter(document_file=document)
    # if not exists:
    #     return Document.objects.create(document_file=document)
    
    # return exists
    try:
        doc = Document.objects.create(document_file=document)
        return doc
    except Exception as e:
        raise exceptions.CustomException(f"Instance not created {e}")

@transaction.atomic
def create_subscription(
    *,
    student_id,
    course_id,
    payment_method,
    subscription_type,
    start_date):
    student = selectors.get_specific_user(student_id)
    course = selectors.get_specific_course(course_id)


    subscription = Subscription.objects.create(
        student=student,
        course=course,
        payment_method=payment_method,
        subscription_type=subscription_type,
    )
    return subscription
