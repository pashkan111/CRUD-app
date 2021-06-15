from django.db.models import fields
from rest_framework import serializers
from .models import User, Post
from djoser.serializers import UserCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password')


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserSerialiserWithToken(UserSerialiser):
    token = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = ('id', 'username', 'token')

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class PostSerializer(serializers.ModelSerializer): 
    class Meta: 
        model=Post
        fields=['id', 'name', 'text']


