from django.shortcuts import render
from courses.models import Category

def index(request):
    
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    
    return render(request, "frontend/index.html", context)
