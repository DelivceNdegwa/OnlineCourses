from django.db import models
from django.contrib.auth import get_user_model
from .constants import USER, ADMIN


User = get_user_model()


ROLE_CHOICES = (
    (ADMIN, "Admin"),
    (USER, "User")
)


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    role_type = models.IntegerField(choices=ROLE_CHOICES, default=USER)

    def __str__(self):
        return self.role_type
