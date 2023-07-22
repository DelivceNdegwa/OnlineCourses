from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    
    pending_stats_dict = {
        'type': 'pending',
        'count': 0,
        'description': 'Courses <br> pending'
    }
    completed_stats_dict = {
        'type': 'completed',
        'count': 0,
        'description': 'Courses <br> completed'
    }
    
    courses_stats_list = [pending_stats_dict, completed_stats_dict]
    
    context = {
        "courses_stats": courses_stats_list
    }
    return render(request, "dashboard/customer/home.html", context)

@login_required
def student_learning(request):
    context = {
        
    }
    return render(request, "dashboard/customer/my_learning.html", context)
