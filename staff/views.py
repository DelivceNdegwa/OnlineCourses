from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def home(request):
    context = {
        
    }
    return render(request, "dashboard/admin/home.html", context)