from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Video)
admin.site.register(models.VideoDocument)
admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Section)