from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "profile")
    age = models.PositiveIntegerField(null = True, blank = True)
    email = models.EmailField(max_length = 255,null = True, blank = True)
    contact_no = models.CharField(max_length = 15,null = True, blank = True)
    dob = models.DateField(null = True, blank = True)
    is_deleted = models.BooleanField(default = False)

