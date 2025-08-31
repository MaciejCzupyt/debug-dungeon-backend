from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    SHIRT_SIZES = {
        "S": "Small",
        "M": "Medium",
        "L": "Large",
    }

    title = models.CharField(max_length=50, unique=True)
    # TODO probably add a repository_link
    description = models.TextField()
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    tags = models.ManyToManyField(Tag, related_name="projects")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    repository_link = models.URLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.content[:16]
    def __str__(self):
        return f"{self.user.username},{self.project.title},{self.created}"
