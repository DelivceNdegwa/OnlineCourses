from typing import Optional
from django.db.models import Count
from base import selectors, exceptions, utils
from courses.models import (
    SystemSettings,
    Category,
    Course,
    CourseStudent,
    Section,
    Video,
    Document,
    VideoDocument
)


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


def get_specific_course(id: int) -> Course:
    return selectors.get_specific_object(Course, id)


def get_course_sections(filter_params: Optional[dict]=None, extra_fields: list=[]):
    allowed_fields = utils.get_model_field_names(Section)

    # if extra_fields:
    #     allowed_fields += extra_fields

    if not filter_params['course__id']:
        raise exceptions.CustomException("Please provide a course")
    return selectors.get_objects(Section, filter_params, allowed_fields, extra_fields)


def get_course_students(filter_params: Optional[dict]):
    allowed_fields = ['id', 'course__id', 'student__id', 'active']
    if not filter_params['course']:
        raise exceptions.CustomException("course__id is a mandatory field")
    return selectors.get_objects(CourseStudent, filter_params , allowed_fields)


def get_courses_with_active_students():
    return Course.objects.filter(coursestudent__active=True).annotate(num_active_students=Count('coursestudent__student'))


def get_specific_section(section_id):
    return selectors.get_specific_object(Section, section_id)

def get_sections(filter_params: Optional[dict]=None) -> Section:
    allowed_fields = ['id', 'course__id']
    selectors.get_objects(Section, filter_params, allowed_fields)


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
    selectors.get_objects(Video, filter_params, allowed_fields).first()
    

def get_specific_document(filter_params: Optional[dict]=None) -> Document:
    allowed_fields = ['id']
    selectors.get_objects(Document, filter_params, allowed_fields).first()



def get_video_documents(filter_params: Optional[dict]=None, extra_fields: list=[]):
    allowed_fields = utils.get_model_field_names(VideoDocument, filter_params)
    allowed_fields += ['section__id']
    if not filter_params['section__id']:
        raise exceptions.CustomException("Please provide a section")
    
    # if filter_params['video__id'] or filter_params['document__id']:
    return selectors.get_objects(VideoDocument, filter_params, allowed_fields, extra_fields)
    
    # raise exceptions.CustomException("Either provide a video or a section for this section item")
