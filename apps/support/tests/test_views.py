from datetime import datetime

from django.core.cache import cache
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.support.models import RightholderAppeal, HelpAppeal
from apps.support.choices import RightholderAppealEvents, HelpAppealEvents
from apps.user.tests.mixins import UserProviderMixin

UserModel = get_user_model()


class RightholderAppealAPIViewTest(UserProviderMixin, APITestCase):
    return_value_of_timezone_now = datetime(2023, 10, 10, 11, 0, 0)
    maxDiff = None

    def setUp(self):
        self.url = reverse('support:create-rightholder-appeal')

    def tearDown(self):
        cache.clear()

    def test_create_rightholder_appeal_without_auth_user(self):
        response = self.client.post(self.url, data={
            'organization': 'organization',
            'contact_person': 'contact_person',
            'email': 'test@gmail.com',
            'release_url': 'release_url',
            'document_url': 'document_url',
            'explanation': 'explanation',
            'message': 'message',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rightholder_appeal = RightholderAppeal.objects.filter(
            organization='organization',
            email='test@gmail.com'
        ).first()

        self.assertIsNone(rightholder_appeal.user)
        self.assertIsNone(rightholder_appeal.assigned)

        self.assertTrue(
            rightholder_appeal.rightholderappeal_history.filter(
                event=RightholderAppealEvents.OPEN
            ).exists()
        )

    def test_create_rightholder_appeal_auth_user(self):
        auth_resp = self.client.post(reverse('authentication:login'), data={
            'username': 'username',
            'password': 'password',
        })

        self.assertEqual(auth_resp.status_code, status.HTTP_200_OK)

        self.assertIn('access', auth_resp.json())
        self.assertIn('refresh', auth_resp.json())

        access_token = auth_resp.json()['access']

        response = self.client.post(self.url, data={
            'organization': 'organization',
            'contact_person': 'contact_person',
            'email': 'test@gmail.com',
            'release_url': '{}',
            'document_url': '{}',
            'explanation': 'explanation',
            'message': 'message',
        }, headers={
            'Authorization': f'Bearer {access_token}'
        })

        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(response.content, {})

        rightholder_appeal = RightholderAppeal.objects.filter(
            organization='organization',
            email='test@gmail.com'
        ).first()

        self.assertEqual(rightholder_appeal.user, self.user)
        self.assertIsNone(rightholder_appeal.assigned)

        self.assertTrue(
            rightholder_appeal.rightholderappeal_history.filter(
                event=RightholderAppealEvents.OPEN
            ).exists()
        )

    def test_create_rightholder_appeal_with_incorrect_email(self):
        response = self.client.post(self.url, data={
            'organization': 'organization',
            'contact_person': 'contact_person',
            'email': 'test',
            'release_url': 'release_url',
            'document_url': 'document_url',
            'explanation': 'explanation',
            'message': 'message',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(response.content, {"errors": [
            {
                "message": "Введіть коректну адресу електронної пошти.",
                "location": "email"
            },
        ]})


class HelpAppealAPIViewTest(UserProviderMixin, APITestCase):
    return_value_of_timezone_now = datetime(2023, 10, 10, 11, 0, 0)
    maxDiff = None

    def setUp(self):
        self.url = reverse('support:create-help-appeal')

    def tearDown(self):
        cache.clear()

    def test_create_help_appeal_without_auth_user(self):
        response = self.client.post(self.url, data={
            'title': 'organization',
            'email': 'test@gmail.com',
            'message': 'message',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        help_appeal = HelpAppeal.objects.filter(
            title='organization',
            email='test@gmail.com'
        ).first()

        self.assertIsNone(help_appeal.user)
        self.assertIsNone(help_appeal.assigned)

        self.assertTrue(
            help_appeal.helpappeal_history.filter(
                event=HelpAppealEvents.OPEN
            ).exists()
        )

    def test_create_help_appeal_auth_user(self):
        auth_resp = self.client.post(reverse('authentication:login'), data={
            'username': 'username',
            'password': 'password',
        })

        self.assertEqual(auth_resp.status_code, status.HTTP_200_OK)

        self.assertIn('access', auth_resp.json())
        self.assertIn('refresh', auth_resp.json())

        access_token = auth_resp.json()['access']

        response = self.client.post(self.url, data={
            'title': 'organization',
            'email': 'test@gmail.com',
            'message': 'message',
        }, headers={
            'Authorization': f'Bearer {access_token}'
        })

        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(response.content, {})

        help_appeal = HelpAppeal.objects.filter(
            title='organization',
            email='test@gmail.com'
        ).first()

        self.assertEqual(help_appeal.user, self.user)
        self.assertIsNone(help_appeal.assigned)

        self.assertTrue(
            help_appeal.helpappeal_history.filter(
                event=HelpAppealEvents.OPEN
            ).exists()
        )

    def test_create_help_appeal_with_incorrect_email(self):
        response = self.client.post(self.url, data={
            'title': 'organization',
            'email': 'test',
            'message': 'message',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(response.content, {"errors": [
            {
                "message": "Введіть коректну адресу електронної пошти.",
                "location": "email"
            },
        ]})
