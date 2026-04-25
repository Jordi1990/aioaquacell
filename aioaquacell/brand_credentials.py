"""Class which holds credentials for a specific brand."""

from dataclasses import dataclass


@dataclass(kw_only=True)
class BrandCredentials:
    """Class which holds credentials for a specific brand."""

    name: str
    client_id: str
    pool_id: str
    identity_pool_id: str
