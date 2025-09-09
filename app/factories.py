import factory
from faker import Faker
from django.contrib.auth.models import User
from .models import Project, Tag, Comment

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"User{n}")
    password = factory.PostGenerationMethodCall("set_password", "password")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"Tag{n}")


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Sequence(lambda n: f"Project{n}")
    description = factory.Faker("paragraph")
    shirt_size = factory.Iterator(["S", "M", "L"])
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(TagFactory(), TagFactory())

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(TagFactory(), TagFactory())


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    content = factory.Faker("paragraph")
    repository_link = factory.Faker("url")
    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)

