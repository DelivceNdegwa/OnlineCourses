from django.urls import path
from staff import views

app_name="staff"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('categories/', views.categories, name="categories"),
    path('courses/', views.courses, name="courses"),
    path('categories/<category_id>', views.read_update_category, name="read_update_category"),
    path("categories/<category_id>/delete", views.delete_category, name="delete_category")
]

