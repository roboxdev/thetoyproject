import factory
from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
    is_active = True
    is_staff = False
    is_superuser = False
    username = factory.Faker('user_name')
