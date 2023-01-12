import os

from django.db import migrations
from django.utils import timezone
from django.contrib.auth import get_user_model


def create_superuser(apps, schema_editor):
    for i in range(1, 3):
        superuser = get_user_model()(
            is_active=True,
            is_superuser=True,
            is_staff=True,
            username=os.environ.get(f'ADMIN_USERNAME{i}'),
            email=os.environ.get(f'ADMIN_EMAIL{i}'),
            last_login=timezone.now(),
        )
        superuser.set_password(os.environ.get(f'ADMIN_PASSWORD{i}'))
        superuser.save()


def create_user(apps, schema_editor):
        user = get_user_model()(
            is_active=True,
            is_superuser=False,
            is_staff=False,
            username=os.environ.get(f'USER_USERNAME'),
            email=os.environ.get(f'USER_EMAIL'),
            last_login=timezone.now(),
        )
        user.set_password(os.environ.get("USER_PASSWORD"))
        user.save()


class Migration(migrations.Migration):
    dependencies = []

    operations = [migrations.RunPython(create_user), migrations.RunPython(create_superuser)]
