""" Parses data from the Aquacell API. """
import json
import logging
import string
import asyncio
import botocore
from aiohttp import ClientSession

from aioaquacell.aws_cognito_authenticator import AwsCognitoAuthenticator
from aioaquacell.aws_signature_request import AwsSignatureRequest
from aioaquacell.const import Brand, SUPPORTED_BRANDS, REGION_NAME, ALL_SOFTENERS
from aioaquacell.exceptions import NotAuthenticated, ApiException, AuthenticationFailed
from aioaquacell.softener import Softener

_LOGGER = logging.getLogger(__name__)


class AquacellApi:

    def __init__(self, session: ClientSession, brand: Brand = Brand.AQUACELL):
        self.session = session
        self.id_token = None

        _LOGGER.debug("Using authentication details from %s", brand)
        self.client_id = SUPPORTED_BRANDS[brand].client_id
        self.pool_id = SUPPORTED_BRANDS[brand].pool_id
        self.identity_pool_id = SUPPORTED_BRANDS[brand].identity_pool_id

        self.authenticator = AwsCognitoAuthenticator(
            REGION_NAME, self.client_id, self.pool_id, self.identity_pool_id
        )

    """ Authenticate using a previous obtained refresh token. """
    async def authenticate_refresh(self, refresh_token) -> string:
        return await self.__authenticate(None, None, refresh_token)

    """" Authenticate using username and password. """
    async def authenticate(self, user_name, password) -> string:
        return await self.__authenticate(user_name, password, None)

    async def __authenticate(self, user_name, password, refresh_token) -> string:
        _LOGGER.debug("Authenticating with %s - %s (%s)", user_name, password, refresh_token)
        try:
            if refresh_token is None:
                # Use asyncio_to_thread to make sure aiobotocore doesn't block event loop.
                token = await asyncio.to_thread(self.authenticator.get_new_token, user_name, password)
            else:
                token = await asyncio.to_thread(self.authenticator.refresh_token, refresh_token)

            self.id_token = token.id_token
            return token.refresh_token
        except botocore.exceptions.ClientError as e:
            _LOGGER.exception("Exception while authenticating")
            if e.response['Error']['Code'] == 'NotAuthorizedException':
                raise AuthenticationFailed(e)
            else:
                raise ApiException(e)

    async def get_all_softeners(self) -> list[Softener]:
        if self.id_token is None:
            raise NotAuthenticated()

        try:
            credentials = await asyncio.to_thread(self.authenticator.get_credentials, self.id_token)
            request = AwsSignatureRequest(
                credentials.aws_access_key_id,
                credentials.aws_secret_access_key,
                credentials.aws_session_token,
                REGION_NAME,
            )

            response = await request.request(ALL_SOFTENERS, self.session)

            json_response = json.loads(response)

            softeners = []

            _LOGGER.debug(json_response)
            for softener_as_json in json_response:
                softeners.append(Softener(softener_as_json))

            return softeners
        except botocore.exceptions.ClientError as e:
            _LOGGER.exception("Exception while retrieving softeners")
            raise ApiException(e)
