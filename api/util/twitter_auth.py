from fastapi.security import OAuth2AuthorizationCodeBearer


class TwitterOAuth2(OAuth2AuthorizationCodeBearer):
    auth_endpoint: str = 'https://twitter.com/i/oauth2/authorize'
    token_endpoint: str = 'https://api.twitter.com/2/oauth2/token'

    def __init__(self, scopes: list[str]):
        super().__init__(
            authorizationUrl=self.auth_endpoint,
            tokenUrl=self.token_endpoint,
            scopes={scope: scope for scope in scopes}
        )
