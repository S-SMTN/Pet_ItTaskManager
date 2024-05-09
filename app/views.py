from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from app.forms import PositionSearchForm, WorkerSearchForm, WorkerCreationForm, WorkerChangeForm, TaskForm
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
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Position.objects.all().prefetch_related("workers")
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    queryset = Position.objects.all().prefetch_related("workers")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("app:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("app:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("app:position-list")

    def get_context_data(self, **kwargs) -> dict:
        context = super(PositionDeleteView, self).get_context_data(**kwargs)
        position = self.get_object()
        if position.workers.count() > 0:
            deletion_restricted = True
            context["deletion_restricted"] = deletion_restricted
        return context


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Worker.objects.all().prefetch_related("tasks").select_related("position")
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


def worker_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    worker = get_object_or_404(Worker, pk=pk)
    tasks = Task.objects.filter(assignees=worker).prefetch_related("assignees", "task_type")
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "worker": worker,
        "tasks": tasks,
        "paginator": paginator,
        "page_obj": page_obj,
        "is_paginated": True
    }

    return render(request, "app/worker_detail.html", context=context)


def unassign_task_from_worker_page(
    request: HttpRequest,
    worker_id: int,
    task_id: int
) -> HttpResponse:
    worker = Worker.objects.get(id=worker_id)
    task = Task.objects.get(id=task_id)
    worker.tasks.remove(task)
    return HttpResponseRedirect(reverse_lazy("app:worker-detail", args=[worker_id]))


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerChangeForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("app:worker-list")

    def get_context_data(self, **kwargs) -> dict:
        context = super(WorkerDeleteView, self).get_context_data(**kwargs)
        worker = self.get_object()
        if worker.tasks.count() > 0:
            deletion_restricted = True
            context["deletion_restricted"] = deletion_restricted
        return context


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = TaskType.objects.all().prefetch_related("task_set")
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    queryset = TaskType.objects.all().prefetch_related("task_set__assignees")


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("app:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("app:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("app:task-type-list")

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskTypeDeleteView, self).get_context_data(**kwargs)
        task_type = self.get_object()
        if task_type.task_set.count() > 0:
            deletion_restricted = True
            context["deletion_restricted"] = deletion_restricted
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.all().prefetch_related("assignees", "task_type")
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(username__icontains=name)
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.all().prefetch_related("assignees", "task_type")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("app:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("app:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("app:task-list")

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskDeleteView, self).get_context_data(**kwargs)
        task = self.get_object()
        if task.assignees.count() > 0:
            deletion_restricted = True
            context["deletion_restricted"] = deletion_restricted
        return context
