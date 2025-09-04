from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from backend.permissions import IsOwnerOrReadOnly, IsSelfOrReadOnly
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView

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

    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated, IsSelfOrReadOnly]

    def list(self, request, *args, **kwargs):
        return Response(
            {"detail": "Retrieving list of users is unavailable"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def current_user(request):
    """
    Returns the currently logged-in user
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class LoginView(APIView):
    # authentication_classes = []  # disable DRF auth check
    permission_classes = []      # allow anyone to call

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"detail": "Login successful"}, status=200)
        return JsonResponse({"detail": "Invalid credentials"}, status=400)


class LogoutView(APIView):
    # authentication_classes = []  # disable DRF auth check
    permission_classes = []      # allow anyone to call

    def post(self, request):
        logout(request)
        return JsonResponse({"detail": "Logout successful"}, status=200)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        project = self.get_object()
        comments = project.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


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


# method for setting csrf token
@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})
