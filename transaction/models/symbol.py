

import uuid
from django.db import models



class Symbol(models.Model):

    symbol_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    name = models.CharField(
        max_length=20,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name