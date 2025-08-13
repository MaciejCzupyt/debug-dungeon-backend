from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=16)


class Project(models.Model):
    SHIRT_SIZES = {
        "S": "Small",
        "M": "Medium",
        "L": "Large",
    }

    title = models.CharField(max_length=50)
    description = models.TextField()
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    tags = models.ManyToManyField(Tag, related_name="projects")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class Comment(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField()
    repository_link = models.URLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
