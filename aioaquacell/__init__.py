"""Init."""

from .aquacell_api import AquacellApi, Softener
from .const import SUPPORTED_BRANDS, Brand
from .exceptions import (
    ApiException,
    AquacellApiException,
    AuthenticationFailed,
    NotAuthenticated,
)

__all__ = [
    "AquacellApi",
    "Softener",
    "ApiException",
    "AuthenticationFailed",
    "NotAuthenticated",
    "AquacellApiException",
    "SUPPORTED_BRANDS",
    "Brand",
]
