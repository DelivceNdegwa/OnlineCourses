from typing import Optional
from base import selectors, exceptions, utils
from django.contrib.auth.models import User
from courses.models import SystemSettings, Category, Course, Section, Video,Document


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
    return selectors.get_objects(Category, filter_params, allowed_fields)


def get_specific_course(id: int) -> Course:
    return selectors.get_specific_object(Course, id)


def get_course_sections(filter_params: Optional[dict]=None):
    allowed_fields = utils.get_model_field_names(Section)
    if not filter_params['course']:
        raise exceptions.CustomException("Please provide a course")
    return selectors.get_objects(Section, filter_params, allowed_fields)

# def get_course_students(course_id: int) -> Queryset[User]:
    
def get_specific_section(filter_params: Optional[dict]=None) -> Section:
    allowed_fields = ['id', 'course']
    selectors.get_objects(Section, filter_params, allowed_fields).first()


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
    allowed_fields = ['id', 'section']
    selectors.get_objects(Video, filter_params, allowed_fields).first()
