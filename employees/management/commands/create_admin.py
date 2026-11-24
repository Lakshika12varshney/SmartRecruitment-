
import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a superuser using Render environment variables"

    def handle(self, *args, **options):
        if os.getenv("CREATE_ADMIN") != "True":
            self.stdout.write("Admin creation is disabled.")
            return

        username = os.getenv("ADMIN_USERNAME")
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not all([username, email, password]):
            raise CommandError("Admin environment variables are missing.")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        if created:
            user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS("Admin account is ready.")
        )
