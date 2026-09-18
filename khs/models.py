from datetime import datetime


class User:
    def __init__(self, email, password_hash, role="user"):
        self.email = email
        self.password = password_hash
        self.role = role
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "created_at": self.created_at
        }


class ChatMessage:
    def __init__(self, user_id, role, content):
        self.user_id = user_id
        self.role = role
        self.content = content
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        }


class AuditLog:
    def __init__(self, user_id, action, metadata=None):
        self.user_id = user_id
        self.action = action
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "action": self.action,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
