from django import forms
from courses.models import Category, SystemSettings, Course, Section


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
        fields = '__all__'


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title']
