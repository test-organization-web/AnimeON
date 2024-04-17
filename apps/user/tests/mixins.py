from apps.user.models import User


class UserProviderMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='username', email='email@example.com')
        cls.user.set_password('password')
        cls.user.save(update_fields=['password'])
