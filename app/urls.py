from django.urls import path

from app.views import index, PositionListView, PositionCreateView, PositionUpdateView, PositionDeleteView, \
    WorkerListView

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
]

app_name = "app"
