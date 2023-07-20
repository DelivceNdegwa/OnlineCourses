from django.urls import path
from django.contrib.auth.views import LogoutView
from users import views
from online_courses import settings

app_name = "users"
urlpatterns = [
    path('register/', views.register, name='sign-up'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name="login"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
]
