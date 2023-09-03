from django.urls import path
from . import views

app_name="customer"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('learning/', views.student_learning, name="learning"),
    path('learning/<int:course_id>', views.course_lesson_session, name="course-session"),
    path("learning/<int:course_id>/<int:lesson_id>", views.course_lesson_specific_session, name="course-session-specific"),
]
