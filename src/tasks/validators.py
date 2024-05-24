from src.tasks.models import Task


def validate_task(data: dict) -> bool:
    if not all(hasattr(Task, name) for name in data.keys()):
        return False
    title, description = data.get('title'), data.get('description')
    if not title or not description:
        return False
    if len(title) > 32:
        return False
    return True
