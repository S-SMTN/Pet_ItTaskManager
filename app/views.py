from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from app.forms import PositionSearchForm
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
