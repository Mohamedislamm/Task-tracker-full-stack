import logging

logger = logging.getLogger(__name__)

MAX_TASK_DESCRIPTION_LENGTH = 255
MIN_TASK_DESCRIPTION_LENGTH = 1


def validate_task_description(description):
    if not description:
        return False
    if not isinstance(description, str):
        return False
    if len(description) < MIN_TASK_DESCRIPTION_LENGTH:
        return False
    if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
        logger.warning(f"Task description exceeds max length: {len(description)}")
        return False
    return True


def validate_task_id(task_id):
    if task_id is None:
        return False
    if not isinstance(task_id, int):
        return False
    if task_id <= 0:
        logger.warning(f"Invalid task ID: {task_id}")
        return False
    return True


def paginate_query(query, page=1, per_page=50, max_per_page=100):
    if page < 1:
        page = 1
    if per_page < 1 or per_page > max_per_page:
        per_page = 50
    return query.paginate(page=page, per_page=per_page, error_out=False)


def sanitize_string(text, max_length=None):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    if max_length and len(text) > max_length:
        text = text[:max_length]
    return text


def format_datetime(dt):
    if dt is None:
        return None
    return dt.isoformat()


def get_boolean_param(param_value, default=False):
    if isinstance(param_value, bool):
        return param_value
    if isinstance(param_value, str):
        return param_value.lower() in ('true', '1', 'yes', 'on')
    return default
