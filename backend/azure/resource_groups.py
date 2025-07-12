"""Azure Resource Group management helpers."""
from azure.mgmt.resource import ResourceManagementClient

from .credentials import get_flask_credential

class ResourceGroupManager:
    """Operations for Azure resource groups."""

    def __init__(self, subscription_id: str) -> None:
        credential = get_flask_credential()
        self._client = ResourceManagementClient(credential, subscription_id)

    def list_groups(self) -> list[dict]:
        """Return resource groups for the subscription."""

        groups = self._client.resource_groups.list()
        return [
            {
                "id": g.id,
                "name": g.name,
                "location": g.location,
            }
            for g in groups
        ]

