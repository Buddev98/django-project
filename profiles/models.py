from django.db import models

# Create your models here.
class UserProfile(models.Model):
    profile_picture = models.FileField(upload_to='profiles/')