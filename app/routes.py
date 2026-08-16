import logging
from flask import Blueprint, render_template, request, redirect, jsonify
from sqlalchemy import func
from models import db
from models.task import Task
from app.utils import validate_task_description, validate_task_id

logger = logging.getLogger(__name__)
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return _handle_task_action()

    try:
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        logger.error(f"Error fetching tasks: {e}", exc_info=True)
        return render_template('index.html', tasks=[], error="Failed to load tasks")


def _handle_task_action():
    try:
        action = request.form.get('action', '').strip()
        task_id = request.form.get('task_id', type=int)
        description = request.form.get('description', '').strip()

        if action == 'add':
            if not validate_task_description(description):
                logger.warning("Invalid task description provided")
                return redirect('/')

            new_task = Task(description=description)
            db.session.add(new_task)
            db.session.commit()
            logger.info(f"Task created: ID={new_task.id}")

        elif action == 'toggle':
            if not validate_task_id(task_id):
                logger.warning(f"Invalid task ID for toggle: {task_id}")
                return redirect('/')

            task = Task.query.get(task_id)
            if task:
                task.completed = not task.completed
                db.session.commit()
                logger.info(f"Task {task_id} toggled to {task.completed}")
            else:
                logger.warning(f"Task {task_id} not found for toggle")

        elif action == 'delete':
            if not validate_task_id(task_id):
                logger.warning(f"Invalid task ID for delete: {task_id}")
                return redirect('/')

            task = Task.query.get(task_id)
            if task:
                db.session.delete(task)
                db.session.commit()
                logger.info(f"Task {task_id} deleted")
            else:
                logger.warning(f"Task {task_id} not found for delete")
        else:
            logger.warning(f"Unknown action: {action}")
    except Exception as e:
        logger.error(f"Error processing task action: {e}", exc_info=True)
        db.session.rollback()

    return redirect('/')


@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 50

        query = Task.query.order_by(Task.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        total_tasks = Task.query.count()
        completed_count = db.session.query(func.count(Task.id)).filter(Task.completed == True).scalar() or 0

        return jsonify({
            'tasks': [task.to_dict() for task in paginated.items],
            'pagination': {
                'total': total_tasks,
                'pages': paginated.pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev
            },
            'stats': {
                'total': total_tasks,
                'completed': completed_count,
                'pending': total_tasks - completed_count
            }
        })
    except Exception as e:
        logger.error(f"Error fetching tasks API: {e}", exc_info=True)
        return jsonify({'error': 'Failed to fetch tasks'}), 500


@tasks_bp.route('/health', methods=['GET'])
def health_check():
    try:
        Task.query.first()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 503
