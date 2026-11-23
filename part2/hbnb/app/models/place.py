#!/usr/bin/python3
"""Place entity module."""
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    """Represents a rental property listing in HBnB."""

    def __init__(
        self,
        title: str,
        description: str,
        price: float,
        latitude: float,
        longitude: float,
        owner: User,
    ):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []    # Place "1" -- "0..*" Review : receives
        self.amenities = []  # Place "0..*" -- "0..*" Amenity : features

        owner.add_place(self)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip() or len(value.strip()) > 100:
            raise ValueError("title is required and must be at most 100 characters.")
        self._title = value.strip()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if value is None:
            self._description = ""
        elif isinstance(value, str):
            self._description = value.strip()
        else:
            raise ValueError("description must be a string.")

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or float(value) <= 0:
            raise ValueError("price must be a positive value.")
        self._price = float(value)

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not (-90.0 <= float(value) <= 90.0)
        ):
            raise ValueError("latitude must be between -90.0 and 90.0.")
        self._latitude = float(value)

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not (-180.0 <= float(value) <= 180.0)
        ):
            raise ValueError("longitude must be between -180.0 and 180.0.")
        self._longitude = float(value)

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, value: User):
        if value is None or not isinstance(value, User):
            raise ValueError("owner must be a valid User instance.")
        self._owner = value

    @property
    def owner_id(self) -> str:
        """Convenience accessor matching Part 1 UML owner_id attribute."""
        return self.owner.id

    def add_review(self, review):
        """Associate a Review with this place."""
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity: Amenity):
        """Associate an Amenity with this place."""
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be a valid Amenity instance.")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
