from django.urls import path
from subscriptions import views

app_name = "subscription"
urlpatterns = [
    path("subscription/", views.subscribe, name="subscription"),
    path("subscription/pay/<int:subscription_id>", views.pay_subscription, name="pay-subscription")
]
