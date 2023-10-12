class AquacellApiException(Exception):
    """ Base exception for Aquacell API """


class NotAuthenticated(AquacellApiException):
    """ Not authenticated exception. """


class ApiException(AquacellApiException):
    """ Api error. """


class AutenticationFailed(AquacellApiException):
    """ Authentication failed. """
