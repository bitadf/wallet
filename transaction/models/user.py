import uuid
from django.db import models


class User(models.Model):

    user_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name