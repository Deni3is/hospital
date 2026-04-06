from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Device, Patient


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


class DashboardTabsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="doctor",
            password="StrongPassword123",
        )
        self.client.force_login(self.user)

        Patient.objects.create(
            gender=Patient.Gender.MALE,
            birth_date="1990-04-06",
        )
        Device.objects.create(
            uid1="UID-001",
            uid2="UID-002",
            uid3="UID-003",
            brand=Device.Brand.GE,
            model="Vivid S70",
            name="Ultrasound Room 1",
        )

    def test_dashboard_shows_patients_tab_by_default(self):
        response = self.client.get(reverse("dashboard"))

        self.assertContains(response, "Пациенты")
        self.assertContains(response, "Male")
        self.assertNotContains(response, "Vivid S70")

    def test_dashboard_can_switch_to_devices_tab(self):
        response = self.client.get(reverse("dashboard"), {"tab": "devices"})

        self.assertContains(response, "Устройства")
        self.assertContains(response, "Vivid S70")
        self.assertNotContains(response, "Male")


class CreateDemoUserCommandTests(TestCase):
    def test_command_creates_demo_user(self):
        call_command("create_demo_user")

        user = get_user_model().objects.get(username="doctor")
        self.assertTrue(user.check_password("StrongPassword123"))

    def test_command_updates_existing_user_password(self):
        user = get_user_model().objects.create_user(
            username="doctor",
            password="old-password",
        )

        call_command("create_demo_user", "--password", "NewPassword456")

        user.refresh_from_db()
        self.assertTrue(user.check_password("NewPassword456"))


class PatientFormViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="doctor",
            password="StrongPassword123",
        )
        self.client.force_login(self.user)

    def test_patient_create_page_uses_date_input(self):
        response = self.client.get(reverse("patient_add"))

        self.assertContains(response, 'type="date"')

    def test_patient_can_be_created(self):
        response = self.client.post(
            reverse("patient_add"),
            {
                "gender": Patient.Gender.FEMALE,
                "birth_date": "1994-02-15",
            },
        )

        self.assertRedirects(response, reverse("dashboard") + "?tab=patients")
        self.assertEqual(Patient.objects.count(), 1)

    def test_patient_birth_date_cannot_be_in_future(self):
        future_date = timezone.localdate() + timedelta(days=1)

        response = self.client.post(
            reverse("patient_add"),
            {
                "gender": Patient.Gender.MALE,
                "birth_date": future_date.isoformat(),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Дата рождения не может быть в будущем.")
        self.assertEqual(Patient.objects.count(), 0)

    def test_patient_can_be_updated(self):
        patient = Patient.objects.create(
            gender=Patient.Gender.MALE,
            birth_date="1990-01-01",
        )

        response = self.client.post(
            reverse("patient_edit", args=[patient.pk]),
            {
                "gender": Patient.Gender.OTHER,
                "birth_date": "1991-05-20",
            },
        )

        self.assertRedirects(response, reverse("dashboard") + "?tab=patients")
        patient.refresh_from_db()
        self.assertEqual(patient.gender, Patient.Gender.OTHER)
        self.assertEqual(str(patient.birth_date), "1991-05-20")
