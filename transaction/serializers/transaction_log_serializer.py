from rest_framework import serializers
from transaction.models import ( TransactionLog)
class TransactionLogSerializer(serializers.ModelSerializer):

    transactionId = serializers.UUIDField(source="transaction_id")
    walletId = serializers.UUIDField(source="wallet.wallet_id")
    userId = serializers.UUIDField(source="wallet.user.user_id")
    transactionType = serializers.CharField(source="transaction_type")

    class Meta:
        model = TransactionLog
        fields = [
            "transactionId",
            "walletId",
            "userId",
            "amount",
            "transactionType",
            "created_at"
        ]