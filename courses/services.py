from django.db import transaction

from courses.models import SystemSettings, Category, Section
from courses import selectors


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
        "course__id": course_id,
        "title": title
    }
    section = selectors.get_course_sections(filter_params)
    if section:
        return section[0]
    
    section = Section.objects.create(
        title=title,
        course=course
    )
    return section