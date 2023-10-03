import aiohttp
from aiohttp import ClientSession
from requests_aws4auth import AWS4Auth
from aws_request_signer import AwsRequestSigner


class AwsSignatureRequest:
    def __init__(self, access_key, secret_key, session_token, region_name):
        self.region_name = region_name
        self.session_token = session_token
        self.secret_key = secret_key
        self.access_key = access_key

    async def request(self, url, session: ClientSession = None):
        auth = AWS4Auth(
            self.access_key,
            self.secret_key,
            self.region_name,
            "execute-api",
            session_token=self.session_token,
        )

        request_signer = AwsRequestSigner(
            self.region_name,
            self.access_key,
            self.secret_key,
            "execute-api",
            self.session_token,
        )

        if session is None:
            session = aiohttp.ClientSession()
        headers = {}

        signed_headers = request_signer.sign_with_headers("GET", url, headers)

        async with session:
            async with session.get(url, headers=signed_headers) as response:
                return await response.text()
