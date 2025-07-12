"""Subscription data model."""

from dataclasses import dataclass


@dataclass
class Subscription:
    """Represents an Azure subscription."""

    id: str
    name: str
