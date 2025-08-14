from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, Project, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


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
