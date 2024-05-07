from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from app.models import Position, Worker, TaskType, Task


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


class PositionListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "position_list"
    template_name = "app/position_list.html"
    queryset = Position.objects.all().prefetch_related("workers")
    paginate_by = 10
