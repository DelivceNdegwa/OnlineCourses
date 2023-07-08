from django.shortcuts import render
from courses.models import Category

def index(request):
    categories = Category.objects.all()[:5]
    context = {
        
    }
    
    return render(request, "frontend/index.html", context)
