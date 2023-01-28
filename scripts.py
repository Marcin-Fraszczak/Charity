import os
from random import choices, randint

import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app import models

User = get_user_model()


def check_if_taken(name, counter, admin=False):
    email = f'{name}{counter}@gmail.com'
    existing_users = User.objects.filter(email=email)
    if existing_users:
        counter += 1
        email = check_if_taken(name, counter, admin)
    return email


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

    email = check_if_taken(name, 1, admin)
    password = "Testpass123"

    user = User(email=email, username=email)
    user.set_password(password)
    user.is_active = 1
    user.is_staff = admin
    user.is_superuser = admin
    user.save()

    return user, password


def create_categories():
    categories = ["zabawki", "AGD", "żywność", "ubrania", "sprzęt sportowy", "lekarstwa", "złom", "broń", "amunicja"]
    for cat in categories:
        models.Category.objects.create(name=cat)
        print(cat)


def create_institutions():
    categories = [cat for cat in models.Category.objects.all()]
    institutions = [
        ("Biedni Szwajcarzy", "Wymiarowy basen w domu każdego Szwjcara", 1),
        ("Kasztanowy domek", "Świetlice środowiskowe dla dzieci", 1),
        ("Animals", "Opieka nad porzuconymi zwierzakami", 1),
        ("Życie z wystawki", "Byle co, byle za darmo", 1),
        ("Dzieciaki na zewnątrz", "Krzewienie kultury fizycznej i aktywności na świeżym powietrzu wśród młodzieży", 1),
        ("Dżihad", "Szybka droga do raju", 2),
        ("Caritas", "Pomoc potrzebującym w kraju i za granicą", 2),
        ("WOŚP", "Wielka Orkiestra", 2),
        ("Heniu", "Szuka złomu i małego AGD", 3),
        ("Roman", "Szuka części do Passata", 3),
        ("Stefan", "Zbiera na piwo", 3),
        ("Zyta", "Chce czuć się bezpiecznie na Wildzie", 3),
    ]
    for inst in institutions:
        institution = models.Institution(
            name=inst[0],
            description=inst[1],
            type=inst[2],
        )
        institution.save()
        random_cats = choices(categories, k=randint(1, 4))
        institution.categories.set(random_cats)
        institution.save()
        print(f'{inst[0]}: {inst[1]}')


def populate():
    print(f'=' * 60)
    user, password = create_user(admin=False)
    print(f'User created:')
    print(f'email: \t {user.email}')
    print(f'password: {password}')
    print(f'=' * 60)
    superuser, password = create_user(admin=True)
    print(f'Superuser created:')
    print(f'email: \t {superuser.email}')
    print(f'password: {password}')
    print(f'=' * 60)
    print("Created categories:")
    create_categories()
    print(f'=' * 60)
    print("Created institutions:")
    create_institutions()
    print(f'=' * 60)
    print("END OF DATA\n\n")


def say_hello():
    print("hello")


if __name__ == '__main__':
    populate()
