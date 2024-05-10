from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from app.forms import WorkerCreationForm
from app.models import Position


class FormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position")
        self.form_data = {
            "username": "test_username",
            "position": self.position,
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password_123",
            "password2": "test_password_123",
        }

    def test_worker_creation_form(self) -> None:
        form = WorkerCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_create_worker(self) -> None:
        self.user = get_user_model().objects.create_user(
            username=self.form_data.get("username"),
            password=self.form_data.get("password1"),
            position=self.form_data.get("position"),
            first_name=self.form_data.get("first_name"),
            last_name=self.form_data.get("last_name")
        )
        self.client.force_login(self.user)
        self.client.post(
            reverse("app:worker-create"),
            data=self.form_data
        )
        new_user = get_user_model().objects.get(
            username=self.form_data.get("username")
        )

        self.assertEqual(
            new_user.first_name,
            self.form_data.get("first_name")
        )
        self.assertEqual(
            new_user.last_name,
            self.form_data.get("last_name")
        )
        self.assertEqual(
            new_user.position,
            self.form_data.get("position")
        )
