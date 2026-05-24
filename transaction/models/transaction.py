
import uuid
from django.db import models
from .user import User


from .wallet import Wallet

class TransactionLog(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAW = "WITHDRAW", "Withdraw"
    
    transaction_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False ,
        unique=True
    )
    refrence_key = models.CharField(
        max_length=100,
        unique=True ,
        null=False
        
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name="transactions"
    )
 

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices
    )
    amount = models.DecimalField(
        max_digits=32,
        decimal_places=16,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

