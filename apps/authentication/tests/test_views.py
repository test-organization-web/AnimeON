from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.user.tests.mixins import UserProviderMixin

UserModel = get_user_model()


class UserRegisterViewAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('authentication:register')

    def test_register_success_user(self):
        response = self.client.post(self.url, data={
            'username': 'username', 'email': 'test@gmail.com', 'password': 'password', 'password_repeat': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())
        user = UserModel.objects.filter(username='username', email='test@gmail.com').first()
        self.assertIsNotNone(user)

    def test_password_not_match(self):
        response = self.client.post(self.url, data={
            'username': 'test', 'email': 'test@gmail.com', 'password': 'password', 'password_repeat': 'password1'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {"errors": [
            {
                "message": "Password Does not match",
                "location": "password_repeat"
            },
        ]})

    def test_user_already_exist(self):
        UserModel.objects.create(username='test', email='test@example.com')

        response = self.client.post(self.url, data={
            'username': 'test', 'email': 'test@gmail.com', 'password': 'password',
            'password_repeat': 'password1'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {"errors": [
            {
                "message": "A user with that username already exists.",
                "location": "username"
            },
        ]})

    def test_user_email_already_exist(self):
        UserModel.objects.create(username='test', email='test@example.com')

        response = self.client.post(self.url, data={
            'username': 'test1', 'email': 'test@example.com', 'password': 'password',
            'password_repeat': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {"errors": [
            {
                "message": "user з таким email вже існує.",
                "location": "email"
            },
        ]})

    def test_empty_required_fields(self):
        response = self.client.post(self.url, data={
            'password': 'password',
            'password_repeat': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(response.content, {"errors": [
            {
                "message": "Це поле обов'язкове.",
                "location": "username"
            },
            {
                "message": "Це поле обов'язкове.",
                "location": "email"
            },
        ]})


class UserLoginViewAPIViewTest(UserProviderMixin, APITestCase):
    def setUp(self):
        self.url = reverse('authentication:login')

    def test_success_login(self):
        response = self.client.post(self.url, data={
            'username': 'username',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

    def test_wrong_password(self):
        response = self.client.post(self.url, data={
            'username': 'username',
            'password': 'test'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertJSONEqual(response.content, {
            'detail': 'Не знайдено жодного облікового запису по наданих облікових даних'
        })

    def test_wrong_username(self):
        response = self.client.post(self.url, data={
            'username': 'username1',
            'password': 'test'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertJSONEqual(response.content, {
            'detail': 'Не знайдено жодного облікового запису по наданих облікових даних'
        })
