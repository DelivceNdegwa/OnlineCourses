from typing import Optional
from courses.models import SystemSettings


# Create System Setting
def create_system_setting(one_time_fee, monthly_fee) -> SystemSettings:
    system_settings = SystemSettings.objects.filter(id=1)
    if not system_settings:
        SystemSettings.objects.create(
            one_time_fee=one_time_fee,
            monthly_fee=monthly_fee
        )