import re

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "role"]

    def get_role(self, obj):
        profile = getattr(obj, "profile", None)
        return profile.role if profile else "user"


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        error_messages={
            "required": "Username обов'язковий.",
            "blank": "Username не може бути порожнім.",
            "max_length": "Username не може бути довшим за 150 символів.",
        },
    )
    first_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        error_messages={
            "max_length": "Ім'я не може бути довшим за 150 символів.",
        },
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        error_messages={
            "max_length": "Прізвище не може бути довшим за 150 символів.",
        },
    )
    email = serializers.EmailField(
        max_length=254,
        error_messages={
            "required": "Email обов'язковий.",
            "blank": "Email не може бути порожнім.",
            "invalid": "Введіть коректну email-адресу.",
            "max_length": "Email не може бути довшим за 254 символи.",
        },
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        error_messages={
            "required": "Пароль обов'язковий.",
            "blank": "Пароль не може бути порожнім.",
            "min_length": "Пароль має містити щонайменше 8 символів.",
            "max_length": "Пароль не може бути довшим за 128 символів.",
        },
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        error_messages={
            "required": "Підтвердження пароля обов'язкове.",
            "blank": "Підтвердження пароля не може бути порожнім.",
        },
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Користувач з таким username вже існує.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Користувач з таким email вже існує.")
        return value

    def validate_password(self, value):
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Пароль має містити хоча б одну велику літеру."
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Пароль має містити хоча б одну малу літеру."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Пароль має містити хоча б одну цифру.")
        return value

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password_confirmation"):
            raise serializers.ValidationError(
                {"password_confirmation": "Паролі не збігаються."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        return User.objects.create_user(**validated_data)
