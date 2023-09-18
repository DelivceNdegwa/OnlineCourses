from typing import Optional, Any
from django.db.models import Count
from django.contrib.auth import get_user_model
from base import selectors, exceptions, utils
from courses.models import (
    SystemSettings,
    Category,
    Course,
    CourseStudent,
    Section,
    Video,
    Document,
    VideoDocument,
    Subscription
)


User = get_user_model()


# System Settings
def get_system_settings_current():
    return selectors.get_current(SystemSettings)


# Category
def get_categories(filter_params: Optional[dict]=None):
    allowed_fields = utils.get_model_field_names(Course)
    return selectors.get_objects(Category, filter_params, allowed_fields)

def get_specific_category(id: int) -> Category:
    return selectors.get_specific_object(Category, id)


# Courses
def get_courses(filter_params: Optional[dict]=None):
    allowed_fields = utils.get_model_field_names(Course)
    return selectors.get_objects(Course, filter_params, allowed_fields)

def get_category_courses(category_id: int) -> Any:
    try:
        category = Category.objects.prefetch_related('courses').get(id=category_id)
        return category.courses.all()
    except Category.DoesNotExist as exc:
        raise exceptions.CustomException(exc)


def get_specific_course(id: int) -> Course:
    return selectors.get_specific_object(Course, id)


# def get_course_sections(filter_params: Optional[dict]=None, extra_fields: list=[]):
#     allowed_fields = utils.get_model_field_names(Section)
    
#     if extra_fields:
#         allowed_fields += extra_fields

#     if not filter_params['course__id']:
#         raise exceptions.CustomException("Please provide a course")
#     return selectors.get_objects(Section, filter_params, allowed_fields, extra_fields)


def get_course_students(filter_params: Optional[dict]):
    allowed_fields = ['id', 'course__id', 'student__id', 'active']
    if not filter_params['course']:
        raise exceptions.CustomException("course__id is a mandatory field")
    return selectors.get_objects(CourseStudent, filter_params , allowed_fields)


# def get_courses_with_active_students():
#     return Course.objects.filter(coursestudent__active=True).annotate(num_active_students=Count('coursestudent__student'))

# Sections
def get_sections(filter_params: Optional[dict]=None) -> Section:
    allowed_fields = ['id', 'course__id']
    selectors.get_objects(Section, filter_params, allowed_fields)

def get_course_sections(course_id: int) -> Any:
    try:
        course = Course.objects.prefetch_related('sections').get(id=course_id)
        return course.sections.all()
    except Course.DoesNotExist as exc:
        raise exceptions.CustomException(exc)


def get_specific_section(section_id):
    return selectors.get_specific_object(Section, section_id)


def get_section_videos(filter_params: Optional[dict]=None):
    allowed_fields = utils.get_model_field_names(Video)
    if not filter_params['section']:
        raise exceptions.CustomException("Please provide a section")
    return selectors.get_objects(Video, filter_params, allowed_fields)


def get_section_documents(filter_params: Optional[dict]=None):
    allowed_fields = utils.get_model_field_names(Document)
    if not filter_params['section']:
        raise exceptions.CustomException("Please provide a section")
    return selectors.get_objects(Document, filter_params, allowed_fields)


def get_specific_video(filter_params: Optional[dict]=None) -> Video:
    allowed_fields = ['id']
    return selectors.get_objects(Video, filter_params, allowed_fields).first()
    

def get_specific_document(filter_params: Optional[dict]=None) -> Document:
    allowed_fields = ['id']
    return selectors.get_objects(Document, filter_params, allowed_fields).first()


# Lessons
def get_lessons(filter_params: Optional[dict]=None, extra_fields: list=[]):
    allowed_fields = utils.get_model_field_names(VideoDocument, filter_params)
    allowed_fields += ['section__id']
    if not filter_params['section__id']:
        raise exceptions.CustomException("Please provide a section")
    
    # if filter_params['video__id'] or filter_params['document__id']:
    return selectors.get_objects(VideoDocument, filter_params, allowed_fields, extra_fields)
    # raise exceptions.CustomException("Either provide a video or a section for this section item")

def get_section_lessons(section_id: int) -> Any:
    try:
        section = Section.objects.prefetch_related('lessons').get(id=section_id)
        return section.lessons.all()
    except Section.DoesNotExist as exc:
        raise exceptions.CustomException(exc)


def get_specific_lesson(lesson_id: int):
    """
        Used to get an instance of VideoDocument, which stores lessons
        Needs only one argument, that is the lesson_id, which will be an ID of a Video Document instance

        Example: 
            from course import selectors
            
            test_id = 10\n
            lesson = selectors.get_specific_lesson(test_id)
    """
    return selectors.get_specific_object(VideoDocument, lesson_id)


def get_all_users() -> Any:
    return User.objects.all()


def get_specific_user(user_id: int) -> User:
    try:
        user = selectors.get_specific_object(User, user_id)
        return user
    except User.DoesNotExist as exc:
        raise exceptions.CustomException(exc)


def get_all_subscriptions(filter_params: Optional[dict]=None, extra_fields = None) -> Any:
    allowed_fields = utils.get_model_field_names(Subscription, filter_params)

    if extra_fields is not None and type(extra_fields) is list:
        allowed_fields += extra_fields

    return selectors.get_objects(Video, filter_params, allowed_fields)


def get_specific_subscription(subscription_id: int) -> Subscription:
    try:
        subscription = selectors.get_specific_object(Subscription, subscription_id)
        return subscription
    except Subscription.DoesNotExist as exc:
        raise exceptions.CustomException(exc)

# STUDENT COURSES
def get_student_courses(filter_params: Optional[dict] = None, extra_fields = None) -> Any:
    allowed_fields = utils.get_model_field_names(CourseStudent, filter_params)

    if extra_fields is not None and type(extra_fields) is list:
        allowed_fields += extra_fields

    return selectors.get_objects(CourseStudent, filter_params, allowed_fields)

def get_specific_student_course(student_course_id: int) -> CourseStudent:
    try:
        student_course_details = selectors.get_specific_object(CourseStudent, student_course_id)
        return student_course_details
    except Exception as exc:
        raise exceptions.CustomException(exc)


def get_courses_with_active_students():
    return get_student_courses({"active": True}).distinct().count()