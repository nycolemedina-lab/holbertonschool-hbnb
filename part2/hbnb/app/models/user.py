#!/usr/bin/python3
"""BaseModel module defining common attributes and lifecycle methods."""
import uuid
from datetime import datetime, timezone


class BaseModel:
    """Base class for all HBnB domain entities."""

    def __init__(self):
        self.id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        self.created_at = now
        self.updated_at = now

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data: dict):
        """Update attributes from a dictionary and refresh updated_at."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary.")

        protected = {"id", "created_at", "updated_at"}
        for key, value in data.items():
            if key not in protected and hasattr(self, key):
                setattr(self, key, value)
        self.save()
