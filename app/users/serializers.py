from django.contrib.auth.hashers import make_password
from rest_framework import serializers as s
from rest_framework.exceptions import ValidationError

from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email',
                  'first_name', 'last_name', 'is_staff', 'date_joined']
        read_only_fields = ('date_joined', 'is_staff')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        # Применяем встроенные правила валидации пароля Django
        try:
            validate_password(value)
        except ValidationError as e:
            raise s.ValidationError(str(e))
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password'])
        return super().update(instance, validated_data)
