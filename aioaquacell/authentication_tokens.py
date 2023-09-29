"""" Holds the tokens retrieved from authentication. """


class AuthenticationTokens:
    def __init__(self, data):
        self.id_token = data["IdToken"]
        self.refresh_token = data["RefreshToken"]
        self.access_token = data["AccessToken"]
