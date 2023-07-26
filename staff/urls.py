from django.urls import path
from staff import views
from courses import views as course_views

app_name="staff"
urlpatterns = [
    path('home/', views.home, name="home"),
    
    path('categories/', views.categories, name="categories"),
    path('categories/<category_id>', views.read_update_category, name="read_update_category"),
    path("categories/<category_id>/delete", views.delete_category, name="delete_category"),
    
    path('courses/', course_views.admin_courses, name="courses"),
    path('courses/<course_id>', course_views.admin_course_details, name="course_details"),
    path('courses/<course_id>/sections/add', course_views.add_section, name="add_section"),
]

