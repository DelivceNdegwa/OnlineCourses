from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('register/', views.register, name='sign-up'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
