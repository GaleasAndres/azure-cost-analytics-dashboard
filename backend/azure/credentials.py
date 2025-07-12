"""Credential helpers for Azure SDK integration with Flask sessions."""

from flask import session
from typing import Sequence
from azure.core.credentials import AccessToken, TokenCredential


class FlaskSessionCredential(TokenCredential):
    """A simple :class:`~azure.core.credentials.TokenCredential` using Flask session."""

    def __init__(self, scope: Sequence[str]) -> None:
        self._scope = scope

    def get_token(self, *scopes: str, **kwargs: object) -> AccessToken:  # type: ignore[override]
        """Return the :class:`~azure.core.credentials.AccessToken` stored in session."""

        token: str | None = session.get("access_token")
        expires_at: int | None = session.get("token_expires")

        if token is None or expires_at is None:
            raise RuntimeError("User is not authenticated")

        return AccessToken(token, expires_at)


def get_flask_credential() -> FlaskSessionCredential:
    """Create a :class:`FlaskSessionCredential` from the current session."""

    from config import SCOPE

    return FlaskSessionCredential(SCOPE)

