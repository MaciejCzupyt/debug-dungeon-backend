from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True, primary_key=True)

    def clean(self):
        self.name = self.name.strip()
        if not self.name.isalnum():
            raise ValidationError("Tag name must be alphanumeric.")

    def __str__(self):
        return self.name


class Project(models.Model):
    SHIRT_SIZES = {
        "S": "Small",
        "M": "Medium",
        "L": "Large",
    }

    title = models.CharField(max_length=50, unique=True)
    repository_link = models.URLField(blank=True)
    description = models.TextField()
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def clean(self):
        if len(self.title.strip()) < 3:
            raise ValidationError("Title must be at least 3 characters long")
        if len(self.description.strip()) < 10:
            raise ValidationError("Description must be at least 10 characters long")
        if self.repository_link and not self.repository_link.startswith(("http://", "https://")):
            raise ValidationError("Repository link must start with http:// or https://")

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    repository_link = models.URLField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def clean(self):
        if len(self.content.strip()) < 3:
            raise ValidationError("Comment must be at least 3 characters long")
        if self.repository_link and not self.repository_link.startswith(("http://", "https://")):
            raise ValidationError("Repository link must start with http:// or https://")

    def __str__(self):
        return f"{self.user.username},{self.project.title},{self.created}"
