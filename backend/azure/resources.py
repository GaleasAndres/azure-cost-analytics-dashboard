"""Azure resource management helpers."""
from azure.mgmt.resource import ResourceManagementClient
from .credentials import get_flask_credential

class ResourceManager:
    """Operations for Azure resources within a subscription."""

    def __init__(self, subscription_id: str) -> None:
        credential = get_flask_credential()
        self._client = ResourceManagementClient(credential, subscription_id)

    def list_resources(self) -> list[dict]:
        """List resources for the subscription."""

        resources = self._client.resources.list()
        return [
            {
                "id": r.id,
                "name": r.name,
                "type": r.type,
                "location": r.location,
            }
            for r in resources
        ]

    @staticmethod
    def extract_subscription_id(resource_id: str) -> str:
        """Return the subscription ID from a resource ID string."""

        parts = [p for p in resource_id.split("/") if p]
        try:
            idx = parts.index("subscriptions")
            return parts[idx + 1]
        except (ValueError, IndexError) as exc:  # pragma: no cover - defensive
            raise ValueError(f"Invalid resource ID: {resource_id}") from exc

