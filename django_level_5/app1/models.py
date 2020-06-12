from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfileInfo(models.Model):
    # create relationship (don't inherit from user!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # add any additional attributes you want
    portfolio = models.URLField(blank=True)
    picture = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self):
        return self.user.username
