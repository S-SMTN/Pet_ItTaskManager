from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.models import TaskType, Task, Position, Worker

LOGIN_REQUIRED_DIRECT_PATHS = [
    "position-create",
    "worker-list",
    "worker-create",
    "task-type-list",
    "task-type-create",
    "task-list",
    "task-create",
]

LOGIN_REQUIRED_PARAMETRIZED_PATHS = [
    "position-detail",
    "position-update",
    "position-delete",
    "worker-detail",
    "worker-update",
    "worker-delete",
    "task-type-detail",
    "task-type-update",
    "task-type-delete",
    "task-detail",
    "task-update",
    "task-delete",
]


class PublicAppTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position")
        self.user = get_user_model().objects.create(
            username="test_username",
            position=self.position,
            password="test_password"
        )
        self.task_type = TaskType.objects.create(
            name="test_name",
        )
        self.task = Task.objects.create(
            name="test_name",
            description="tesl_description",
            deadline=date(2024, 1, 10),
            is_completed=False,
            priority=1,
            task_type=self.task_type
        )

    def test_login_required(self) -> None:
        respond_logs = dict()
        for path in LOGIN_REQUIRED_DIRECT_PATHS:
            client_response = self.client.get(reverse(f"app:{path}"))
            respond_logs.update({path: client_response.status_code})
        for path in LOGIN_REQUIRED_PARAMETRIZED_PATHS:
            client_response = self.client.get(
                reverse(f"app:{path}", kwargs={"pk": 1})
            )
            respond_logs.update({path: client_response.status_code})
        for path, status in respond_logs.items():
            self.assertNotEqual(
                status,
                200,
                msg=f"Path {path} is free without login!"
            )


class PrivateAppTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position")
        self.user = get_user_model().objects.create(
            username="test_username",
            position=self.position,
            password="test_password"
        )
        self.task_type = TaskType.objects.create(
            name="test_name",
        )
        self.task = Task.objects.create(
            name="test_name",
            description="tesl_description",
            deadline=date(2024, 1, 10),
            is_completed=False,
            priority=1,
            task_type=self.task_type
        )
        self.task.assignees.set((self.user,))
        self.client.force_login(self.user)

    def test_toggle_index(self) -> None:
        num_workers = Worker.objects.count()
        num_positions = Position.objects.count()
        num_task_types = TaskType.objects.count()
        num_tasks = Task.objects.count()

        response = self.client.get(reverse("app:index"))

        self.assertEqual(
            response.context["num_workers"],
            num_workers
        )
        self.assertEqual(
            response.context["num_positions"],
            num_positions
        )
        self.assertEqual(
            response.context["num_task_types"],
            num_task_types
        )
        self.assertEqual(
            response.context["num_tasks"],
            num_tasks
        )

    def test_toggle_position_list(self) -> None:
        positions = Position.objects.all()
        response = self.client.get(reverse("app:position-list"))
        self.assertEqual(
            list(response.context.get("position_list", [])),
            list(positions)
        )

    def test_toggle_worker_list(self) -> None:
        workers = Worker.objects.all()
        response = self.client.get(reverse("app:worker-list"))
        self.assertEqual(
            list(response.context.get("worker_list", [])),
            list(workers)
        )

    def test_toggle_task_type_list(self) -> None:
        task_type = TaskType.objects.all()
        response = self.client.get(reverse("app:task-type-list"))
        self.assertEqual(
            list(response.context.get("tasktype_list", [])),
            list(task_type)
        )

    def test_toggle_task_list(self) -> None:
        task = Task.objects.all()
        response = self.client.get(reverse("app:task-list"))
        self.assertEqual(
            list(response.context.get("task_list", [])),
            list(task)
        )
