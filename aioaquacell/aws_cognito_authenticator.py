"""AWS Cognito authentication and identity management."""

import logging

import boto3
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

    def refresh_token(self, refresh_token: str) -> AuthenticationTokens:
        """Regenerates the token by providing a refresh token."""
        client = boto3.client("cognito-idp", self.region_name)
        resp = client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
            },
            ClientId=self.client_id,
        )
        _LOGGER.debug("Authentication response %s", resp)
        return AuthenticationTokens.from_dict(resp["AuthenticationResult"])

    def get_new_token(self, username: str, password: str) -> AuthenticationTokens:
        """Gets the initial token by providing username and password."""
        client = boto3.client("cognito-idp", self.region_name)
        aws_srp = AWSSRP(
            username=username,
            password=password,
            pool_id=self.pool_id,
            client_id=self.client_id,
            client=client,
        )

        auth_params = aws_srp.get_auth_params()
        resp = client.initiate_auth(
            AuthFlow="USER_SRP_AUTH",
            AuthParameters=auth_params,
            ClientId=self.client_id,
        )

        challenge_response = aws_srp.process_challenge(
            resp["ChallengeParameters"], auth_params
        )

        resp = client.respond_to_auth_challenge(
            ClientId=self.client_id,
            ChallengeName="PASSWORD_VERIFIER",
            ChallengeResponses=challenge_response,
        )
        _LOGGER.debug("Authentication result %s", resp)
        return AuthenticationTokens.from_dict(resp["AuthenticationResult"])

    def get_credentials(self, id_token: str) -> AwsCredentials:
        """Retrieves the AWS credentials to sign a request."""
        client = boto3.client("cognito-identity", self.region_name)
        logins = {
            f"cognito-idp.{self.region_name}.amazonaws.com/{self.pool_id}": id_token
        }

        identity_response = client.get_id(
            IdentityPoolId=self.identity_pool_id, Logins=logins
        )

        credentials_response = client.get_credentials_for_identity(
            IdentityId=identity_response["IdentityId"], Logins=logins
        )
        _LOGGER.debug("Get credentials %s", credentials_response)
        return AwsCredentials.from_dict(credentials_response["Credentials"])
