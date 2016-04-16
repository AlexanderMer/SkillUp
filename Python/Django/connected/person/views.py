from django.shortcuts import render
from person.models import UserProfile
# Create your views here.

def index(request):
    return render(request, "index.html", {})

def details(request, profile_id):
    profile = UserProfile.objects.get(id=profile_id)
    return render(request, "details.html", {'profile': profile})
