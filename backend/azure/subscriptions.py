"""Azure subscription management utilities."""
from azure.mgmt.resource import SubscriptionClient
from .credentials import get_flask_credential
class SubscriptionManager:
    """Helper class for Azure subscription operations."""

    def __init__(self) -> None:
        credential = get_flask_credential()
        self._client = SubscriptionClient(credential)

    def list_subscriptions(self) -> list[dict]:
        """Return all subscriptions available for the signed-in user."""

        subs = self._client.subscriptions.list()
        return [
            {
                "subscription_id": sub.subscription_id,
                "display_name": sub.display_name,
                "state": str(sub.state),
            }
            for sub in subs
        ]

