from django.urls import include, path
from rest_framework import routers

from app import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"tags", views.TagViewSet)
router.register(r"projects", views.ProjectViewSet)
router.register(r"comments", views.CommentViewSet)


urlpatterns = [
    path("users/me", views.current_user),
    path("", include(router.urls)),
    path("csrf/", views.get_csrf)
]
