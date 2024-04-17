from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        password = validated_data['password']
        password2 = validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"password": "Password Does not match"})

        if UserModel.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exist"})
        return validated_data

    def save(self):
        password = self.validated_data['password']

        user = UserModel(email=self.validated_data['email'], username=self.validated_data['username'])
        user.set_password(password)
        user.save()

        return user
