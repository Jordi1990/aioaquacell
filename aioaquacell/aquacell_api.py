"""Parses data from the Aquacell API."""

import asyncio
import json
import logging

from aiohttp import ClientSession
from botocore.exceptions import ClientError

from aioaquacell.aws_cognito_authenticator import AwsCognitoAuthenticator
from aioaquacell.aws_signature_request import AwsSignatureRequest
from aioaquacell.const import ALL_SOFTENERS, REGION_NAME, SUPPORTED_BRANDS, Brand
from aioaquacell.exceptions import ApiException, AuthenticationFailed, NotAuthenticated
from aioaquacell.softener import Softener

_LOGGER = logging.getLogger(__name__)


class AquacellApi:
    """Aquacell API."""

    def __init__(self, session: ClientSession, brand: Brand = Brand.AQUACELL) -> None:
        self.session = session
        self.id_token: str | None = None

        _LOGGER.debug("Using authentication details from %s", brand)
        self.client_id = SUPPORTED_BRANDS[brand].client_id
        self.pool_id = SUPPORTED_BRANDS[brand].pool_id
        self.identity_pool_id = SUPPORTED_BRANDS[brand].identity_pool_id

        self.authenticator = AwsCognitoAuthenticator(
            REGION_NAME, self.client_id, self.pool_id, self.identity_pool_id
        )

    async def authenticate_refresh(self, refresh_token: str) -> str | None:
        """Authenticate using a previous obtained refresh token."""
        return await self.__authenticate(None, None, refresh_token)

    async def authenticate(self, user_name: str, password: str) -> str | None:
        """Authenticate using username and password."""
        return await self.__authenticate(user_name, password, None)

    async def __authenticate(
        self,
        user_name: str | None,
        password: str | None,
        refresh_token: str | None,
    ) -> str | None:
        _LOGGER.debug("Authenticating user %s", user_name)
        try:
            if refresh_token is None:
                token = await asyncio.to_thread(
                    self.authenticator.get_new_token, user_name, password
                )
            else:
                token = await asyncio.to_thread(
                    self.authenticator.refresh_token, refresh_token
                )

            self.id_token = token.id_token
            return token.refresh_token
        except ClientError as e:
            _LOGGER.exception("Exception while authenticating")
            if e.response["Error"]["Code"] == "NotAuthorizedException":
                raise AuthenticationFailed(e) from e
            raise ApiException(e) from e

    async def get_all_softeners(self) -> list[Softener]:
        """Retrieves all softeners."""
        if self.id_token is None:
            raise NotAuthenticated()

        try:
            credentials = await asyncio.to_thread(
                self.authenticator.get_credentials, self.id_token
            )
            request = AwsSignatureRequest(
                credentials.aws_access_key_id,
                credentials.aws_secret_access_key,
                credentials.aws_session_token,
                REGION_NAME,
            )

            response = await request.request(ALL_SOFTENERS, self.session)
            json_response = json.loads(response)

            _LOGGER.debug(json_response)
            return [Softener.from_dict(s) for s in json_response]
        except ClientError as e:
            _LOGGER.exception("Exception while retrieving softeners")
            raise ApiException(e) from e
