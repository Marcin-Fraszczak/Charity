import subprocess

from django.contrib.auth import get_user_model
from django.core.management import call_command

from app import models

User = get_user_model()
counter = {
    "admin": 1,
    "user": 1,
}


def check_if_taken(name, admin=False):
    existing_users = User.objects.filter(email=f'{name}{counter[name]}@gmail.com')
    if existing_users:
        counter[name] += 1
        check_if_taken(name, admin)
    else:
        return f'{name}{counter[name]}@gmail.com'


def create_user(admin=False):
    try:
        admin = bool(admin)
    except Exception as e:
        print(e)
        return None

    if admin:
        name = "admin"
    else:
        name = "user"

    email = check_if_taken(name, admin)
    password = "Testpass123"

    user = User(email=email)
    user.set_password(password)
    user.is_active = 1
    user.is_staff = admin
    user.is_superuser = admin
    user.save()

    return user


def start():
    subprocess.run("pip install -r requirements.txt")
    call_command("migrate", interactive=False)
    user = create_user(admin=False)
    superuser = create_user(admin=True)
    print(f'=' * 60)
    print(f'User created:')
    print(f'email: \t {user.email}')
    print(f'password: {user.password}')
    print(f'=' * 60)
    print(f'Superuser created:')
    print(f'email: \t {superuser.email}')
    print(f'password: {superuser.password}')
    print(f'=' * 60)
    call_command("runserver", interactive=False)
    print("Go check your default web browser")
