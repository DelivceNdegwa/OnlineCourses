from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    ADMIN = 1
    INSTRUCTOR = 2
    STUDENT = 3
    
    ROLE_TYPES = (
        (ADMIN, "Admin"),
        (INSTRUCTOR, "Instructor"),
        (STUDENT, "Student")
    )
    
    role_type = models.IntegerField(choices=ROLE_TYPES, default=STUDENT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
