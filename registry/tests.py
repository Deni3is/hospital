from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="doctor",
            password="StrongPassword123",
        )

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("dashboard"))

        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_user_can_login_through_custom_page(self):
        response = self.client.post(
            reverse("login"),
            {"username": "doctor", "password": "StrongPassword123"},
        )

        self.assertRedirects(response, reverse("dashboard"))
