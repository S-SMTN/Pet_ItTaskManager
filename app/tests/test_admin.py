from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from app.models import Position, TaskType, Task


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.position_developer = Position.objects.create(name="Developer")
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.worker = get_user_model().objects.create_user(
            position=self.position_developer,
            username="worker_username",
            email="email@mail.com",
            password="test1234",
            last_name="last_name",
            first_name="last_name"
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Task",
            description="Task_description",
            deadline=date(2024, 1, 10),
            is_completed=False,
            priority=1,
            task_type=self.task_type
        )


    def test_worker_position_listed(self) -> None:
        url = reverse("admin:app_worker_changelist")
        url_response = self.client.get(url)
        self.assertContains(url_response, self.worker.position)

    def test_worker_detail_position_listed(self) -> None:
        url = reverse(
            "admin:app_worker_change",
            args=[self.worker.id]
        )
        url_response = self.client.get(url)
        self.assertContains(url_response, self.worker.position)
        self.assertContains(url_response, self.worker.first_name)
        self.assertContains(url_response, self.worker.last_name)

    def test_task_listed(self) -> None:
        url = reverse("admin:app_task_changelist")
        url_response = self.client.get(url)
        self.assertContains(url_response, self.task.name)
        self.assertContains(url_response, self.task.description)
        self.assertContains(url_response, "Jan. 10, 2024")
        self.assertContains(url_response, self.task.is_completed)
        self.assertContains(url_response, self.task.priority)
        self.assertContains(url_response, self.task.task_type)


