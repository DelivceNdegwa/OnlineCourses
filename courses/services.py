from typing import Optional
from django.db import transaction

from courses.models import SystemSettings, Category
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


@transaction.atomic
def delete_category(category_id: int):
    category = selectors.get_specific_category(category_id)
    category.delete()
