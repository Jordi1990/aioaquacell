"""" Holds the tokens retrieved from authentication. """


class AuthenticationTokens:
    def __init__(self, data):
        self.id_token = data["IdToken"]
        try:
            self.refresh_token = data["RefreshToken"]
        except KeyError:
            self.refresh_token = None
