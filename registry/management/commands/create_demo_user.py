from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update a demo user for local login."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default="doctor",
            help="Username for the demo user.",
        )
        parser.add_argument(
            "--password",
            default="StrongPassword123",
            help="Password for the demo user.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        user_model = get_user_model()

        user, created = user_model.objects.get_or_create(username=username)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Demo user created: username={username} password={password}"
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo user updated: username={username} password={password}"
            )
        )
