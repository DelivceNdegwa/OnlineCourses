from django.urls import path
from . import views

app_name="customer"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('learning/', views.student_learning, name="learning"),
    path(
        'learning/<int:course_id>/<int:section_id>/<int:lesson_id>',
        views.course_lesson_session,
        name="course-lesson-session"
    ),
]
