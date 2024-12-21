"""Holds the tokens retrieved from authentication."""

from dataclasses import dataclass


@dataclass
class AuthenticationTokens:
    """Holds the tokens retrieved from authentication."""

    def __init__(self, data):
        self.id_token = data["IdToken"]
        try:
            self.refresh_token = data["RefreshToken"]
        except KeyError:
            self.refresh_token = None
