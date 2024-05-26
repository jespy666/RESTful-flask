from .models import Task


def validate_task(data: dict) -> bool:
    # check if data Model has all given params provided in request body
    if not all(hasattr(Task, name) for name in data.keys()):
        return False
    title, description = data.get('title'), data.get('description')
    # check if request body has all required params
    if not title or not description:
        return False
    # check title length
    if len(title) > 32:
        return False
    return True
