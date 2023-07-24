from fastapi import APIRouter, Security, Request
# from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.requests import Request as StarletteRequest
from .config import Settings

router = APIRouter()
settings = Settings()


'''
class TwitterOAuth2(OAuth2AuthorizationCodeBearer):
    auth_endpoint: str = 'https://twitter.com/i/oauth2/authorize'
    token_endpoint: str = 'https://api.twitter.com/2/oauth2/token'

    def __init__(self, scopes: list[str]):
        super().__init__(
            authorizationUrl=self.auth_endpoint,
            tokenUrl=self.token_endpoint,
            scopes={scope: scope for scope in scopes}
        )
'''

# auth_scheme = TwitterOAuth2(scopes=settings.twitter_scopes)

oauth = OAuth()
oauth.register(
    name='twitter',
    client_id=settings.twitter_client_id,
    access_token_url='https://api.twitter.com/2/oauth2/token',
    authorize_url='https://twitter.com/i/oauth2/authorize',
    client_kwargs={
        'token_endpoint_auth_method': 'none',
        'code_challenge_method': 'S256',
        'scope': ' '.join(settings.twitter_scopes)
    }
)


@router.get('/login/twitter')
async def login_via_google(request: StarletteRequest):
    redirect_uri = request.url_for('auth_via_twitter')
    return await oauth.twitter.authorize_redirect(request, redirect_uri)


@router.get('/auth/twitter')
async def auth_via_twitter(request: StarletteRequest):
    token = await oauth.twitter.authorize_access_token(request)
    return token


@router.get('/hello-world')
async def hello_world():
    return dict(message='hello world')
