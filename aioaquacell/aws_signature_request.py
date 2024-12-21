"""Defines the AWS request with sign headers."""

from dataclasses import dataclass
from aiohttp import ClientSession
from aws_request_signer import AwsRequestSigner


@dataclass
class AwsSignatureRequest:
    """Defines the AWS request with sign headers."""

    def __init__(self, access_key, secret_key, session_token, region_name):
        self.region_name = region_name
        self.session_token = session_token
        self.secret_key = secret_key
        self.access_key = access_key

    async def request(self, url, session: ClientSession):
        """Executes signed request."""

        request_signer = AwsRequestSigner(
            self.region_name,
            self.access_key,
            self.secret_key,
            "execute-api",
            self.session_token,
        )

        headers = {}

        signed_headers = request_signer.sign_with_headers("GET", url, headers)

        async with session.get(url, headers=signed_headers) as response:
            return await response.text()
