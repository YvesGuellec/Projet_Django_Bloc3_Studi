import uuid
from django.contrib.auth.models import User
from django.db import models

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f'Profil de {self.user.username}'
