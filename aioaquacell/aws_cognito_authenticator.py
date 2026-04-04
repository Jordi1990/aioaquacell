"""AWS Cognito authentication and identity management."""

import logging

from aiobotocore.session import get_session
from pycognito import AWSSRP

from aioaquacell.authentication_tokens import AuthenticationTokens
from aioaquacell.aws_credentials import AwsCredentials

_LOGGER = logging.getLogger(__name__)


class AwsCognitoAuthenticator:
    """AWS Cognito authentication and identity management."""

    def __init__(self, region_name: str, client_id: str, pool_id: str, identity_pool_id: str) -> None:
        self.region_name = region_name
        self.identity_pool_id = identity_pool_id
        self.client_id = client_id
        self.pool_id = pool_id
        self.session = get_session()

    async def refresh_token(self, refresh_token: str) -> AuthenticationTokens:
        """Regenerates the token by providing a refresh token."""
        async with self.session.create_client("cognito-idp", region_name=self.region_name) as client:
            resp = await client.initiate_auth(
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token,
                },
                ClientId=self.client_id,
            )
        _LOGGER.debug("Authentication response %s", resp)
        return AuthenticationTokens.from_dict(resp["AuthenticationResult"])

    async def get_new_token(self, username: str, password: str) -> AuthenticationTokens:
        """Gets the initial token by providing username and password."""
        # We only use AWSSRP for local SRP crypto, not for network calls.
        # Pass a dummy client to prevent it from creating a boto3 client.
        aws_srp = AWSSRP(
            username=username,
            password=password,
            pool_id=self.pool_id,
            client_id=self.client_id,
            client=object(),
        )
        auth_params = aws_srp.get_auth_params()

        async with self.session.create_client("cognito-idp", region_name=self.region_name) as client:
            resp = await client.initiate_auth(
                AuthFlow="USER_SRP_AUTH",
                AuthParameters=auth_params,
                ClientId=self.client_id,
            )

            challenge_response = aws_srp.process_challenge(
                resp["ChallengeParameters"], auth_params
            )

            resp = await client.respond_to_auth_challenge(
                ClientId=self.client_id,
                ChallengeName="PASSWORD_VERIFIER",
                ChallengeResponses=challenge_response,
            )
        _LOGGER.debug("Authentication result %s", resp)
        return AuthenticationTokens.from_dict(resp["AuthenticationResult"])

    async def get_credentials(self, id_token: str) -> AwsCredentials:
        """Retrieves the AWS credentials to sign a request."""
        logins = {
            f"cognito-idp.{self.region_name}.amazonaws.com/{self.pool_id}": id_token
        }

        async with self.session.create_client("cognito-identity", region_name=self.region_name) as client:
            identity_response = await client.get_id(
                IdentityPoolId=self.identity_pool_id, Logins=logins
            )

            credentials_response = await client.get_credentials_for_identity(
                IdentityId=identity_response["IdentityId"], Logins=logins
            )
        _LOGGER.debug("Get credentials %s", credentials_response)
        return AwsCredentials.from_dict(credentials_response["Credentials"])
