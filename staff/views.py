from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
'''
    The home view contains: A table of current courses subscribed by students, courses generally, notifications, categories 
'''
@staff_member_required
def home(request):
    context = {
        
    }
    return render(request, "dashboard/admin/home.html", context)