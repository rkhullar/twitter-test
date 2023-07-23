from fastapi import APIRouter, Security, Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from .config import Settings

router = APIRouter()
settings = Settings()


class TwitterOAuth2(OAuth2AuthorizationCodeBearer):
    auth_endpoint: str = 'https://twitter.com/i/oauth2/authorize'
    token_endpoint: str = 'https://api.twitter.com/2/oauth2/token'

    def __init__(self, scopes: list[str]):
        super().__init__(
            authorizationUrl=self.auth_endpoint,
            tokenUrl=self.token_endpoint,
            scopes={scope: scope for scope in scopes}
        )


auth_scheme = TwitterOAuth2(scopes=settings.twitter_scopes)


@router.get('/test', include_in_schema=True)
async def test_redirect(request: Request):
    print(request)
    return str(request)


@router.get('/hello-world')
async def hello_world(token: str = Security(auth_scheme)):
    return dict(message='hello world', token=token)
