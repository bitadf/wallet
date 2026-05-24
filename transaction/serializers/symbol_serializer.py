from rest_framework import serializers
from transaction.models import Symbol
from transaction.utils.messages import invalidSymbolNameError
class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = "__all__"
        read_only_fields = ["symbol_id" , "created_at"]

    def validate_name(self,value):
        value = value.upper().strip()
        if len(value) < 1:
            raise serializers.ValidationError(
                invalidSymbolNameError
            )
        if not value.isalnum():
            raise serializers.ValidationError(
                invalidSymbolNameError
            )
        return value