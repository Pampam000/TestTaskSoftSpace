from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def delete(self, *args, **kwargs):
        """
        Instead of actually deleting the user, we set is_active to False
        """
        self.is_active = False
        self.save()
