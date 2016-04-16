from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=150)
    birth_date = models.DateField()
    avatar = models.ImageField(blank=True, upload_to='static/uploads')
    about = models.TextField(blank=True)

    def __str__(self):
        return  self.name
