""" Parses data from the Aquacell API. """
import json

from aiohttp import ClientSession

from aioaquacell.aws_cognito_authenticator import AwsCognitoAuthenticator
from aioaquacell.aws_signature_request import AwsSignatureRequest
from aioaquacell.softener import Softener


class AquacellApi:
    base_url = "https://y7xyrocicl.execute-api.eu-west-1.amazonaws.com"
    all_softeners = f"{base_url}/prod/v1/softeners/all"
    region_name = "eu-west-1"
    client_id = "64kp67l1jo9toeesan7s1sdpae"
    pool_id = "eu-west-1_noZbcE2Av"
    identity_pool_id = "eu-west-1:f44120d5-bd20-4461-b282-1ed637861951"

    def __init__(self, session: ClientSession):
        self.session = session
        self.refresh_token = None
        self.id_token = None
        self.authenticator = AwsCognitoAuthenticator(
            self.region_name, self.client_id, self.pool_id, self.identity_pool_id
        )

    """ Authenticate using a previous obtained refresh token. """

    async def authenticate_refresh(self, refresh_token) -> bool:
        return await self.__authenticate(None, None, refresh_token)

    """" Authenticate using username and password. """

    async def authenticate(self, user_name, password) -> bool:
        return await self.__authenticate(user_name, password, None)

    async def __authenticate(self, user_name, password, refresh_token) -> bool:
        try:
            if refresh_token is None:
                token = await self.authenticator.get_new_token(user_name, password)
            else:
                token = await self.authenticator.refresh_token(refresh_token)

            self.refresh_token = token.refresh_token
            self.id_token = token.id_token
            return True
        except Exception as e:
            print(e)
            return False

    async def get_all_softeners(self) -> list[Softener]:
        if self.id_token is None:
            raise Exception("Not authenticated")

        credentials = await self.authenticator.get_credentials(self.id_token)
        request = AwsSignatureRequest(
            credentials.aws_access_key_id,
            credentials.aws_secret_access_key,
            credentials.aws_session_token,
            self.region_name,
        )

        response = await request.request(self.all_softeners, self.session)

        json_response = json.loads(response)

        softeners = []
        for softener_as_json in json_response:
            softeners.append(Softener(softener_as_json))

        return softeners
