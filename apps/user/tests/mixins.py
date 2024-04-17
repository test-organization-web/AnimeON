from apps.user.models import User


class UserProviderMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='username', email=',@example.com')
        cls.user.set_password('password')
