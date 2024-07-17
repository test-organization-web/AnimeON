from django.test import TestCase
from rest_framework import status


class PingMiddlewareTestCase(TestCase):
    def test_ping_pong_success(self):
        response = self.client.get("/ping/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.content, b'pong')
