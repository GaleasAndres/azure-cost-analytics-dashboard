"""Utilities for authenticating with Azure Active Directory."""

from typing import Optional

from msal import ConfidentialClientApplication

from config import settings


class AzureAuth:
    """Simple wrapper around MSAL for acquiring tokens."""

    def __init__(self) -> None:
        self._app = ConfidentialClientApplication(
            client_id=settings.azure_client_id,
            authority=f"https://login.microsoftonline.com/{settings.azure_tenant_id}",
            client_credential=settings.azure_client_secret.get_secret_value(),
        )

    def get_access_token(self, scope: str) -> Optional[str]:
        """Acquire an access token for the given scope."""
        result = self._app.acquire_token_silent([scope], account=None)
        if not result:
            result = self._app.acquire_token_for_client(scopes=[scope])
        return result.get("access_token") if result else None
