#!/usr/bin/python3
"""Review entity module."""
from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    """Represents a user review for a Place."""

    def __init__(self, text: str, rating: int, place: Place, user: User):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.validate()

        place.add_review(self)
        user.add_review(self)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("text is required and must be a non-empty string.")
        self._text = value.strip()

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int):
        if isinstance(value, bool) or not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("rating must be an integer between 1 and 5.")
        self._rating = value

    @property
    def place(self) -> Place:
        return self._place

    @place.setter
    def place(self, value: Place):
        if value is None or not isinstance(value, Place):
            raise ValueError("place must be a valid Place instance.")
        self._place = value

    @property
    def user(self) -> User:
        return self._user

    @user.setter
    def user(self, value: User):
        if value is None or not isinstance(value, User):
            raise ValueError("user must be a valid User instance.")
        self._user = value

    @property
    def place_id(self) -> str:
        """Convenience accessor matching Part 1 UML place_id attribute."""
        return self.place.id

    @property
    def user_id(self) -> str:
        """Convenience accessor matching Part 1 UML user_id attribute."""
        return self.user.id

    def validate(self):
        """Re-verify all review invariants (from Part 1 UML design)."""
        if not self.text or not (1 <= self.rating <= 5):
            raise ValueError("Review failed validation.")
        if not isinstance(self.place, Place) or not isinstance(self.user, User):
            raise ValueError("Review must reference valid Place and User instances.")
