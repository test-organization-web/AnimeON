from rest_framework import serializers
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    count_viewed_anime = serializers.CharField(source='get_count_viewed_anime')

    class Meta:
        model = UserModel
        fields = ('username', 'count_viewed_anime')


class UserAnimeCountSerializer(serializers.Serializer):
    count_viewed_anime = serializers.IntegerField()


