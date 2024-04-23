from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
    """
        Has a 1-1 relationship with built-in User
        extends built-in user by adding 2 additional fields

    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,)

    # Additional fields
    portfolio_site = models.URLField(blank=True)

    profile_image = models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return "%s is Current User " % self.user.username
