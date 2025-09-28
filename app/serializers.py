from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Comment, Project, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", 'date_joined']
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)

        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        extra_kwargs = {
            "name": {"read_only": True},
        }

    def validate(self, data):
        instance = Tag(**data)

        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, "message_dict") else e.messages)

        return data


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    created = serializers.DateTimeField(format="%d %b %H:%M")
    modified = serializers.DateTimeField(format="%d %b %H:%M")

    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

    def validate(self, data):
        instance = Project(
            title=data.get("title"),
            description=data.get("description"),
            repository_link=data.get("repository_link"),
            shirt_size=data.get("shirt_size"),
            user=self.context["request"].user
        )

        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, "message_dict") else e.messages)

        return data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created = serializers.DateTimeField(format="%d %b %H:%M")
    modified = serializers.DateTimeField(format="%d %b %H:%M")

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

    def validate(self, data):
        instance = Comment(**data)

        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, "message_dict") else e.messages)

        return data

