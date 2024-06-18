from rest_framework import serializers
from .models import News
from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["title", "description", "created_at", "updated_at", "user"]


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']
