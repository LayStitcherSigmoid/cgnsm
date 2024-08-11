from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Administrarion(AbstractUser):

    pass

    def __str__(self):
        return self.username


class Pragmon(models.Model):
    user_created = models.ForeignKey(Administrarion, on_delete=models.RESTRICT, related_name="user_created")
    user_last_updated = models.ForeignKey(Administrarion, on_delete=models.RESTRICT, related_name="user_last_updated")
    time_created = models.DateTimeField(auto_now_add=True)
    time_last_updated = models.DateTimeField(auto_now=True)
    ip_created = models.GenericIPAddressField()
    ip_last_updated = models.GenericIPAddressField()