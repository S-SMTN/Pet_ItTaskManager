from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import Position, TaskType, Task


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.position_developer = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            position=self.position_developer,
            username="worker_username",
            email="email@mail.com",
            password="test1234",
            last_name="last_name",
            first_name="last_name"
        )
        self.today = date(2024, 1, 9)
        self.task_type = TaskType.objects.create(name="Bug")
        self.task_description = "Task_description"
        self.task_1 = Task.objects.create(
            name="Task1",
            description=self.task_description,
            deadline=date(2024, 1, 10),
            is_completed=False,
            priority=1,
            task_type=self.task_type
        )
        self.task_2 = Task.objects.create(
            name="Task2",
            description=self.task_description,
            deadline=date(2024, 1, 10),
            is_completed=True,
            priority=1,
            task_type=self.task_type
        )
        self.task_3 = Task.objects.create(
            name="Task3",
            description=self.task_description,
            deadline=date(2024, 1, 8),
            is_completed=False,
            priority=1,
            task_type=self.task_type
        )
        self.task_4 = Task.objects.create(
            name="Task4",
            description=self.task_description,
            deadline=date(2024, 1, 11),
            is_completed=False,
            priority=2,
            task_type=self.task_type
        )
        self.task_5 = Task.objects.create(
            name="Task5",
            description=self.task_description,
            deadline=date(2024, 1, 10),
            is_completed=False,
            priority=2,
            task_type=self.task_type
        )
        self.task_list = [
            self.task_3,
            self.task_1,
            self.task_5,
            self.task_4,
            self.task_2
        ]

    def test_position_str(self) -> None:
        self.assertEqual(
            str(self.position_developer),
            f"{self.position_developer.name}"
        )

    def test_worker_str(self) -> None:
        self.assertEqual(
            str(self.worker),
            (
                f"{self.worker.username} "
                f"({self.worker.first_name} {self.worker.last_name})"
            )
        )

    def test_task_type_str(self) -> None:
        self.assertEqual(
            str(self.task_type),
            f"{self.task_type.name}"
        )

    def test_task_str(self) -> None:
        self.assertEqual(
            str(self.task_1),
            f"{self.task_1.name}"
        )

    def test_task_ordering(self) -> None:
        self.assertEqual(
            list(Task.objects.all()),
            self.task_list
        )
