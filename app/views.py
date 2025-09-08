from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from backend.permissions import IsOwnerOrReadOnly, IsSelfOrReadOnly
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from django.db.models import Q

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

    @action(detail=True, methods=['get'])
    def all(self, request, username=None):
        user = self.get_object()
        projects = user.project_set.all()
        comments = user.comment_set.all()

        return Response({
            "user": UserSerializer(user).data,
            "projects": ProjectSerializer(projects, many=True).data,
            "comments": CommentSerializer(comments, many=True).data,
        })

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticatedOrReadOnly(), IsSelfOrReadOnly()]

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


def _ensure_tags_exist(tags):
    if not tags:
        return
    for t in tags:
        name = str(t).strip()
        if name:
            Tag.objects.get_or_create(name=name)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        tags = request.data.get("tags", [])
        _ensure_tags_exist(tags)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        tags = request.data.get("tags", None)
        if tags is not None:
            _ensure_tags_exist(tags)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        project = self.get_object()
        comments = project.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Project.objects.all()

        search = self.request.query_params.get('search')
        user = self.request.query_params.get('user')
        shirt_size = self.request.query_params.get('shirt_size')
        tags = self.request.query_params.get('tags')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(user__username__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()
        if user:
            queryset = queryset.filter(user__username=user)
        if shirt_size:
            queryset = queryset.filter(shirt_size=shirt_size)
        if tags:
            tag_list = tags.split(',')
            queryset = queryset.filter(tags__name__in=tag_list).distinct()

        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# method for setting csrf token
@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})
