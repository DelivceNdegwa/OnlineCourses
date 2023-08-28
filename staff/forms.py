from django import forms
from courses.models import Category, SystemSettings, Course, Section, Video, Document


class SystemSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'description', 'thumbnail_image', 'monthly_price', 'one_time_price', 'ready']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_file']
