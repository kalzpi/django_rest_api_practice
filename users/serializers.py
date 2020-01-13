from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "user_permissions",
            "password",
            "groups",
            "date_joined",
            "is_active",
            "last_login",
            "is_superuser",
            "favs",
        )


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "user_permissions",
            "password",
            "groups",
            "date_joined",
            "is_active",
            "last_login",
            "is_superuser",
        )


class WriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "email")

    def validate_first_name(self, value):
        return value.upper()
