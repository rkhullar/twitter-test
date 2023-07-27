from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from .config import Settings
from .depends import ReadTokenData
from .schema.user import TwitterTokenData, TwitterUserData
from .twitter import TwitterAPIClient

router = APIRouter()
settings = Settings()
twitter_client = TwitterAPIClient()

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
async def login_via_twitter(request: Request):
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


@router.get('/debug/token', response_model=TwitterTokenData)
async def debug_token(token_data: ReadTokenData):
    return token_data


@router.post('test/refresh', response_model=dict)
async def write_tweet(token_data: ReadTokenData):
    pass


@router.get('/test/user', response_model=TwitterUserData)
async def read_user(token_data: ReadTokenData):
    response_data = await twitter_client.request(method='get', url='/users/me', auth_data=token_data)
    return response_data['data']


@router.post('test/tweet', response_model=dict)
async def write_tweet(token_data: ReadTokenData):
    pass


@router.post('test/direct-message', response_model=dict)
async def send_direct_message(token_data: ReadTokenData):
    pass
