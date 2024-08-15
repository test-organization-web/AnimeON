from django.contrib.auth import get_user_model


class UserProviderMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(username='username', email='email@example.com')
        cls.user.set_password('password')
        cls.user.save(update_fields=['password'])
