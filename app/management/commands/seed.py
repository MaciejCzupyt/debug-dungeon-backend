from django.core.management.base import BaseCommand
from app.factories import UserFactory, TagFactory, ProjectFactory, CommentFactory


class Command(BaseCommand):
    help = "Seed the database with fake data"

    def add_arguments(self, parser):
        # parser.add_argument("--users", type=int, default=10, help="Number of to create")
        parser.add_argument("--tags", type=int, default=20, help="Number of to create")
        # parser.add_argument("--projects", type=int, default=100, help="Number of to create")
        parser.add_argument("--comments", type=int, default=100, help="Number of to create")

    def handle(self, *args, **kwargs):
        users = UserFactory.create_batch(kwargs["users"])
        tags = TagFactory.create_batch(kwargs["tags"])
        projects = ProjectFactory.create_batch(kwargs["projects"])
        comments = CommentFactory.create_batch(kwargs["comments"])
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(users)} users, {len(tags)} tags, {len(projects)} projects, {len(comments)} comments,"
        ))
