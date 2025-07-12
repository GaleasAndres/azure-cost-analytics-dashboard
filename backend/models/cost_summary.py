"""Cost summary data model."""

from dataclasses import dataclass


@dataclass
class CostSummary:
    """Represents aggregated cost information."""

    total: float
