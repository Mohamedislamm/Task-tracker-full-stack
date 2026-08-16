from datetime import datetime
from models import db


class Task(db.Model):
    __tablename__ = 'tasks'
    __table_args__ = (
        db.Index('idx_completed', 'completed'),
        db.Index('idx_created_at', 'created_at'),
    )

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False, index=True)
    completed = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Task {self.id}: {self.description[:50]}>'

    def toggle(self):
        self.completed = not self.completed
        return self

    @staticmethod
    def get_statistics():
        from sqlalchemy import func

        total = Task.query.count()
        completed = Task.query.filter_by(completed=True).count()
        pending = total - completed

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }
