from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from backend.permissions import IsOwnerOrReadOnly

from .models import Comment, Project, Tag
from .serializers import (
    CommentSerializer,
    ProjectSerializer,
    TagSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Retrieving users by ID is unavailable"},
            status=status.HTTP_404_NOT_FOUND
        )

    def list(self, request, *args, **kwargs):
        return Response(
            {"detail": "Retrieving list of users is unavailable"},
            status=status.HTTP_404_NOT_FOUND
        )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    '''
        TODO
        overwrite create methods so that the user is set automatically or we can bypass this issue
        user = serializers.StringRelatedField()
        currently when we specify this in serializers.py, retrieving the model means we get a user string instead of id,
        but when trying to create a new instance of the object we cannot specify the user and he remains null
    '''


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    '''
        TODO
        overwrite create methods so that the user is set automatically or we can bypass this issue
        user = serializers.StringRelatedField()
        currently when we specify this in serializers.py, retrieving the model means we get a user string instead of id,
        but when trying to create a new instance of the object we cannot specify the user and he remains null
    '''

    def destroy(self, request, *args, **kwargs):
        # but now we're gonna do some additional checks BEFORE that

        # TODO:
        # 1. we need to know what user sent the request
        # 2. we need to know if the user is an owner of all the comments this request refers to
        # 3. if NOT then we return 401 early
        print("WE ARE DELETING, ARENT WE??")

        # this should not change the behaviour
        super().destroy(request, *args, **kwargs)
