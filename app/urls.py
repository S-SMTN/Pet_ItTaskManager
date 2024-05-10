from django.urls import path

from app.views import index, PositionListView, PositionCreateView, PositionUpdateView, PositionDeleteView, \
    WorkerListView, worker_detail_view, unassign_task_from_worker_page, PositionDetailView, WorkerCreateView, \
    WorkerUpdateView, WorkerDeleteView, TaskTypeListView, TaskTypeDetailView, TaskTypeCreateView, TaskTypeUpdateView, \
    TaskTypeDeleteView, TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("positions", PositionListView.as_view(), name="position-list"),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create",
    ),
    path(
        "positions/<int:pk>/detail/",
        PositionDetailView.as_view(),
        name="position-detail",
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "position/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list",
    ),
    path(
        "workers/<int:pk>/",
        worker_detail_view,
        name="worker-detail",
    ),
    path(
        "workers/<int:worker_id>/unassign/<int:task_id>",
        unassign_task_from_worker_page,
        name="worker-unassign-task",
    ),
    path(
        "workers/create",
        WorkerCreateView.as_view(),
        name="worker-create",
    ),
    path(
        "workers/<int:pk>/update",
        WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "workers/<int:pk>/delete",
        WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
    path(
        "task_types/",
        TaskTypeListView.as_view(),
        name="task-type-list",
    ),
    path(
        "task_type/<int:pk>/detail/",
        TaskTypeDetailView.as_view(),
        name="task-type-detail",
    ),
    path(
        "task_type/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create",
    ),
    path(
        "task_type/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "task_type/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list",
    ),
    path(
        "task/<int:pk>/detail/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "task/create/",
        TaskCreateView.as_view(),
        name="task-create",
    ),
    path(
        "task/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "task/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete",
    ),
]

app_name = "app"
