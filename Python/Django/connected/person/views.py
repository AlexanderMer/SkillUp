from django.shortcuts import render
from person.models import UserProfile
from person.forms import UserForm, UserProfileForm

# Create your views here.

def index(request):
    profiles  = UserProfile.objects.all()
    return render(request, "index.html", {'profiles': profiles})

def details(request, profile_id):
    profile = UserProfile.objects.get(id=profile_id)
    return render(request, "details.html", {'profile': profile})

def register(request):
    if request.POST:
        pass
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render(request, 'register.html', {'user_form': user_form,
                                                 'profile_form': profile_form})