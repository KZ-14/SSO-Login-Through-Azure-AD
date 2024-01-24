from django.db import models

# Create your models here.

class CustomPermission(models.Model):
    class Meta:
        permissions = [
            ("can_access_auth_url", "Can access the auth URL"),
        ]

