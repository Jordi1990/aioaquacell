"""Holds AWS credentials to sign a request to AWS services."""

from dataclasses import dataclass


@dataclass
class AwsCredentials:
    """Holds AWS credentials to sign a request to AWS services."""

    def __init__(self, data):
        self.aws_access_key_id = data["AccessKeyId"]
        self.aws_secret_access_key = data["SecretKey"]
        self.aws_session_token = data["SessionToken"]
