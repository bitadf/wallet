from rest_framework import serializers
from transaction.models import Wallet, Symbol
from transaction.utils.messages import symbolNotFoundError
class WalletSerializer(serializers.ModelSerializer):
    symbol_name = serializers.CharField(write_only=True)
    user_id = serializers.UUIDField(
        
    )


    class Meta:
        model = Wallet
        fields = ["wallet_id" , "symbol_name" , "balance" , "user_id" ]
        read_only_fields = ["wallet_id" , "balance"]
    
    def validate_symbol_name(self , value):
        value = value.upper().strip()
        if not Symbol.objects.filter(name = value).exists():
            raise serializers.ValidationError(symbolNotFoundError)
        return value