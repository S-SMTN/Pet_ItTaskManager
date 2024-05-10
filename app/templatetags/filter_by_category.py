from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter
def filter_task_by_is_completed(model: QuerySet, is_completed: bool) -> QuerySet:
    return model.filter(is_completed=is_completed)
