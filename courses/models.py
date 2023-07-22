from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from courses import constants
from courses.utils import VideoProcessor

from users.models import Role


User = get_user_model()


class SystemSettings(models.Model):
    one_time_fee = models.DecimalField(decimal_places=1, max_digits=10)
    monthly_fee = models.DecimalField(decimal_places=1, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        verbose_name_plural = 'SystemSettings'
        ordering = ['-created_at']
        
    # def save(self, *args, **kwargs):
    #         if not self.pk and SystemSettings.objects.exists():
    #             raise ValidationError('There is can be only one SystemSetting instance')
    #         return super(SystemSettings, self).save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if self.id == 1:
            try:
                existing_instance = SystemSettings.objects.get(pk=1)
                for field in self._meta.fields:
                    if field.name != 'id':
                        setattr(existing_instance, field.name, getattr(self, field.name))
                existing_instance.save()
            except SystemSettings.DoesNotExist:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    short_description = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name_plural="Categories"
        ordering=['-created_at']
        
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    profile_image = models.ImageField(upload_to='user_profile')
    
    def __str__(self):
        return self.user.username


class Instructor(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    
    def __str__(self):
        return self.profile


class Course(models.Model):
    title = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    number_of_students = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class CourseStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.username}:{self.course.title}"



class Section(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, null=True)
    hls_manifest = models.FileField(upload_to='hls/', blank=True, null=True)
    dash_manifest = models.FileField(upload_to='dash/', blank=True, null=True)
    
    def generate_hls(self):
        video_processor = VideoProcessor(self)
        video_processor.process(constants.HLS)
        return self.hls_manifest.url
    
    def generate_dash(self):
        video_processor = VideoProcessor(self)
        video_processor.process(constants.DASH)
        return self.dash_manifest.url
    
    def __str__(self):
        return f"{self.title}:{self.video_file}"


class Document(models.Model):
    title = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    document_file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        return f"Review for {self.course}"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return f"Question for {self.course}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f"Answer for {self.question}"


class Bookmark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bookmark for {self.course}"


class Completion(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    completion_date = models.DateTimeField()

    def __str__(self):
        return f"Completion for {self.course}"

class Message(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title

class Subscription(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    subscription_type = models.CharField(max_length=100)  # One-time or Monthly
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Subscription for {self.course}"
