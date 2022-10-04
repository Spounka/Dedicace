import random
from .models import User, Celebrity, Fan


def create_dummy_user(i: int, offset: int = 0):
    phone_number = f"+2130000000{i + offset:02}"
    password = "rootuser"
    email = f"admin{i + offset + 1}@admin.com"
    username = f"username{i + offset + 1}"
    user = User.objects.create_user(phone_number=phone_number, email=email, password=password, username=username)
    user.save()
    return user


def create_dummy_celebs(number=10, offset: int = 0):
    for i in range(number):
        celeb = Celebrity.objects.create(user=create_dummy_user(i, offset))
        celeb.save()


def create_dummy_fans(number=10, offset: int = 0):
    for i in range(number):
        wilaya = random.randint(1, 58)
        fan = Fan.objects.create(user=create_dummy_user(i, offset), wilaya=f"{wilaya}")
        fan.save()


def dummy(number=10):
    create_dummy_fans(number // 2)
    create_dummy_celebs(number // 2, offset=number // 2)


def delete_dummy():
    User.objects.exclude(is_superuser=True).all().delete()
    return True
