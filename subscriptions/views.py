from django.shortcuts import render, redirect
from django.urls import reverse
from courses import services, selectors

# Create your views here.
def subscribe(request):
    if request.method == "POST":
        subscription_type = request.POST.get('subscription-type')
        course_id = request.POST.get('course-id')
        payment_method = request.POST.get('payment-choice')
        print(f"SUBSCRIPTION DATA={request.POST}")
        subscription = services.create_subscription(
            student_id=request.user.id,
            course_id=course_id,
            subscription_type=subscription_type,
            payment_method=payment_method,
        )

        url = reverse("subscription:pay-subscription", kwargs={'subscription_id': subscription.id})
        return redirect(url)
        

def pay_subscription(request, subscription_id: int):
    subscription = selectors.get_specific_subscription(subscription_id)
    context = {
        "subscription": subscription
    }
    return render(request, "subscriptions/payment.html", context)