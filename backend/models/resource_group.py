"""Resource group data model."""

from dataclasses import dataclass


@dataclass
class ResourceGroup:
    """Represents an Azure resource group."""

    name: str
