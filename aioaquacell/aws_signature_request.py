"""Defines the AWS request with sign headers."""

from dataclasses import dataclass

from aiohttp import ClientSession
from aws_request_signer import AwsRequestSigner


@dataclass
class AwsSignatureRequest:
    """Defines the AWS request with sign headers."""

    access_key: str
    secret_key: str
    session_token: str
    region_name: str

    async def request(self, url: str, session: ClientSession) -> str:
        """Executes signed request."""
        request_signer = AwsRequestSigner(
            self.region_name,
            self.access_key,
            self.secret_key,
            "execute-api",
            self.session_token,
        )

        signed_headers = request_signer.sign_with_headers("GET", url, {})

        async with session.get(url, headers=signed_headers) as response:
            return await response.text()
