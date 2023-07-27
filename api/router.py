from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from .config import Settings
from .depends import ReadAccessToken, ReadTokenData
from .util import BearerAuth, async_httpx

router = APIRouter()
settings = Settings()


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


@router.get('/login/twitter', include_in_schema=False)
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_via_twitter')
    return await oauth.twitter.authorize_redirect(request, redirect_uri)


@router.get('/auth/twitter', include_in_schema=False)
async def auth_via_twitter(request: Request):
    token_data = await oauth.twitter.authorize_access_token(request)
    for key, value in token_data.items():
        request.session[key] = value
    docs_uri = request.url_for('swagger_ui_html')
    return RedirectResponse(docs_uri)


@router.get('/debug/session')
async def debug_session(request: Request):
    return request.session


@router.get('/hello-world')
async def hello_world(token_data: ReadTokenData):
    response = await async_httpx(method='get', url='https://api.twitter.com/2/users/me', auth=BearerAuth(token_data.access_token))
    response.raise_for_status()
    response_data = response.json()
    return dict(response_data=response_data['data'], token_data=token_data)
