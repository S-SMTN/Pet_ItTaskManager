from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import Worker, Position, TaskType, Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    search_fields = ["username", "email", "first_name", "last_name"]
    list_filter = ["position"]
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "username",
                        "position",
                        "email"
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type"
    ]
    list_filter = [
        "priority",
        "is_completed",
        "task_type"
    ]


admin.site.register(Position)
admin.site.register(TaskType)
