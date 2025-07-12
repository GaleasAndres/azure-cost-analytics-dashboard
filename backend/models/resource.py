"""Resource data model."""

from dataclasses import dataclass


@dataclass
class Resource:
    """Represents an Azure resource."""

    id: str
    name: str
