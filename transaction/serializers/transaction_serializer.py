from rest_framework import serializers

from transaction.models import (Wallet , TransactionLog)
from transaction.utils.messages import (invalidAmountError , walletNotFoundError)

class TransactionSerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()

    amount = serializers.DecimalField(
        max_digits = 32 ,
        decimal_places = 16
    )
    user_id = serializers.UUIDField()
    
    refrence_key = serializers.CharField()
    

    def validate_amount(self , value):
        if value <= 0 :
            raise serializers.ValidationError(
                invalidAmountError
            )
        return value
    
    def validate_wallet_id(self , value):
        if not Wallet.objects.filter(wallet_id = value).exists():
            raise serializers.ValidationError(
                walletNotFoundError
            )
        return value
