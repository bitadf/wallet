import uuid
from django.db import models
from .user import User

from .symbol import Symbol


class Wallet(models.Model):
    wallet_id = models.UUIDField(
        default=uuid.uuid4 ,
        editable=False , 
        unique=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wallets"
    )

    # user_id = models.IntegerField() 

    # symbol_id = models.CharField(
    #     max_length=20
    # )

    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        related_name="wallets"
    )

    balance = models.DecimalField(
        max_digits=32,
        decimal_places=16,
        default=0
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "symbol")