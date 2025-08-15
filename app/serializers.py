from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, Project, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    #user = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = "__all__"
