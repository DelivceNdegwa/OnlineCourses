from django.shortcuts import render, redirect
from courses import services, selectors

# Create your views here.
def subscribe(request):
    if request.method == "POST":
        subscription_type = request.POST.get('subscription-type')
        course_id = request.POST.get('course-id')
        payment_method = request.POST.get('payment-method')
        phone_number = request.POST.get('phone-number')

        services.create_subscription(
            student_id=request.user.id,
            course_id=course_id,
            subscription_type=subscription_type,
            payment_method=payment_method,
        )
        return redirect("frotend:home")