from django.urls import path
from . import views

app_name="frontend"
urlpatterns = [
    path('', views.index, name="home"),
    path('category/<category_id>/course/<course_id>/', views.course_details, name="course-details"),
]