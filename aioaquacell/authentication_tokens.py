"""Holds the tokens retrieved from authentication."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AuthenticationTokens:
    """Holds the tokens retrieved from authentication."""

    id_token: str
    refresh_token: str | None

    @classmethod
    def from_dict(cls, data: dict) -> AuthenticationTokens:
        """Create from AWS Cognito authentication result dict."""
        return cls(
            id_token=data["IdToken"],
            refresh_token=data.get("RefreshToken"),
        )
