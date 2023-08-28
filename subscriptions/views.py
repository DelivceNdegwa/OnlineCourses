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

    student_courses_filter = {
        "student__id": subscription.student.id,
        "course__id": subscription.course.id
    }
    student_courses = selectors.get_student_courses(
        student_courses_filter,
        ["student__id", "course__id"]
    )
    if not student_courses:
        services.add_student_course(
            subscription.student.id,
            subscription.course.id,
            False
        )

    context = {
        "subscription": subscription
    }
    '''
        TODO 
        1. Call STK PUSH ONCE SOMEONE HAS ADDED THE PHONE NUMBER AND PAYMENT METHOD IS
        MPESA, 
        2. AFTER WHICH THE MERCHANT ID OF THE INDIVIDUAL WILL BE RETRIEVED, 
        3. THIS WILL THEN BE USED TO CHECK IF THE USER PAYS, OR NOT, 
        4. IF THEY DO:
            i.  MAKE THE SUBSCRIPTION PAYMENT STATUS COMPLETE
            ii. ACTIVATE STUDENT'S COURSE
    '''
    return render(request, "subscriptions/payment.html", context)