from typing import Dict, Any

from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

UserModel = get_user_model()


class RequestUserRegisterSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'password_repeat']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        password = validated_data['password']
        password_repeat = validated_data['password_repeat']

        if password != password_repeat:
            raise serializers.ValidationError({"password_repeat": "Паролі не співпадають"})

        if UserModel.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "Користувач з таким e-mail вже існує"})
        return validated_data

    def save(self):
        password = self.validated_data['password']

        user = UserModel(email=self.validated_data['email'], username=self.validated_data['username'])
        user.set_password(password)
        user.save()

        return user


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username']


class ResponseUserRegisterSerializer(serializers.Serializer):
    user = UserReadSerializer()
    refresh = serializers.CharField()
    access = serializers.CharField()


class ResponseUserLoginSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserReadSerializer()


class ResponseUserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data['user'] = {
            'username': self.user.username
        }
        return data
