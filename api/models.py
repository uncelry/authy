from django.db import models
import uuid


# Client (pseudo user) model
class Client(models.Model):
    refresh = models.TextField(verbose_name='Refresh token bcrypt', unique=True)
    public_id = models.UUIDField(default=uuid.uuid4)
