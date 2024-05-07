from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from app.models import Position, Worker, TaskType, Task


# Create your views here.


def index(request: HttpRequest) -> HttpResponse:

    num_positions = Position.objects.count()
    num_workers = Worker.objects.count()
    num_task_types = TaskType.objects.count()
    num_tasks = Task.objects.count()

    context = {
        "num_positions": num_positions,
        "num_workers": num_workers,
        "num_task_types": num_task_types,
        "num_tasks": num_tasks
    }

    return render(request, "app/index.html", context=context)
