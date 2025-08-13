from django.urls import include, path
from rest_framework import routers

from app import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"tags", views.TagViewSet)
router.register(r"projects", views.ProjectViewSet)
router.register(r"comments", views.CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
