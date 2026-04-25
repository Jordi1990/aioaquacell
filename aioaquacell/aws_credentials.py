"""Holds AWS credentials to sign a request to AWS services."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AwsCredentials:
    """Holds AWS credentials to sign a request to AWS services."""

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str

    @classmethod
    def from_dict(cls, data: dict) -> AwsCredentials:
        """Create from AWS Cognito credentials response dict."""
        return cls(
            aws_access_key_id=data["AccessKeyId"],
            aws_secret_access_key=data["SecretKey"],
            aws_session_token=data["SessionToken"],
        )
