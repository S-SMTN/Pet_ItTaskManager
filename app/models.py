from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(
        to=Position,
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):

    class Priorities(models.IntegerChoices):
        URGENT = 1, "Urgent"
        HIGH = 2, "High"
        MIDDLE = 3, "Middle"
        LOW = 4, "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(
        choices=Priorities.choices,
        default=Priorities.MIDDLE
    )
    task_type = models.ForeignKey(
        to=TaskType,
        on_delete=models.PROTECT
    )
    assignees = models.ManyToManyField(
        to=Worker,
        related_name="tasks"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["is_completed", "priority", "deadline"]
