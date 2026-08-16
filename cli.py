import sys
import os
from app import create_app
from models import db
from models.task import Task

app = create_app(os.getenv('FLASK_ENV', 'development'))


def init_db():
    with app.app_context():
        print("Initializing database...")
        db.create_all()
        print("Database initialized successfully")


def reset_db():
    with app.app_context():
        if input("Are you sure you want to delete all data? (yes/no): ").lower() == 'yes':
            print("Resetting database...")
            db.drop_all()
            db.create_all()
            print("Database reset successfully")
        else:
            print("Reset cancelled")


def seed_db():
    with app.app_context():
        print("Seeding database with sample data...")

        sample_tasks = [
            "Buy groceries",
            "Complete project report",
            "Review pull requests",
            "Schedule team meeting",
            "Update documentation",
            "Fix bug in authentication",
            "Optimize database queries",
            "Deploy to production"
        ]

        Task.query.delete()

        for i, description in enumerate(sample_tasks):
            task = Task(
                description=description,
                completed=(i % 3 == 0)
            )
            db.session.add(task)

        db.session.commit()
        print(f"Added {len(sample_tasks)} sample tasks")


def show_stats():
    with app.app_context():
        stats = Task.get_statistics()
        print("\n" + "="*50)
        print("Task Tracker Statistics")
        print("="*50)
        print(f"Total Tasks:        {stats['total']}")
        print(f"Completed:          {stats['completed']}")
        print(f"Pending:            {stats['pending']}")
        print(f"Completion Rate:    {stats['completion_rate']:.1f}%")
        print("="*50 + "\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <db|stats>")
        return

    command = sys.argv[1]

    if command == 'db':
        if len(sys.argv) < 3:
            print("Usage: python cli.py db <init|reset|seed>")
            return

        sub_command = sys.argv[2]

        if sub_command == 'init':
            init_db()
        elif sub_command == 'reset':
            reset_db()
        elif sub_command == 'seed':
            seed_db()
        else:
            print(f"Unknown sub-command: {sub_command}")
    elif command == 'stats':
        show_stats()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python cli.py <db|stats>")


if __name__ == '__main__':
    main()
