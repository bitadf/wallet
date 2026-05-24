from rest_framework import serializers
from transaction.models import User
from transaction.utils.messages import (shortUserNameError)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "user_id",
            "created_at"
        ]

    def validate_name(self, value):

        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
               shortUserNameError
            )

        return value