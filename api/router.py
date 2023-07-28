from typing import Annotated

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Body, Request
from fastapi.responses import RedirectResponse

from .config import Settings
from .depends import ReadTokenData
from .schema.user import TwitterTokenData, TwitterUserData
from .twitter import TwitterAPIClient
from .util import async_httpx

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


@router.post('/test/refresh', response_model=TwitterTokenData)
async def refresh_token(token_data: ReadTokenData, request: Request):
    response_data = await twitter_client.request(method='post', url='/oauth2/token', data={
        'refresh_token': token_data.refresh_token,
        'grant_type': 'refresh_token',
        'client_id': settings.twitter_client_id
    })
    for key, value in response_data.items():
        request.session[key] = value
    return TwitterTokenData(**response_data)


@router.get('/user/me', response_model=TwitterUserData)
async def read_user(token_data: ReadTokenData):
    # NOTE: free tier rate limited to 25 requests per 24 hours per user
    # https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference
    response_data = await twitter_client.request(method='get', url='/users/me', auth_data=token_data)
    return response_data['data']


'''
# NOTE: unavailable in free tier

@router.get('/user/lookup', response_model=dict)
async def lookup_user(token_data: ReadTokenData, username: str):
    # https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference
    response_data = await twitter_client.request(method='get', url=f'/users/by/username/{username}', auth_data=token_data)
    return response_data['data']
'''


@router.post('/test/tweet', response_model=dict)
async def write_tweet(token_data: ReadTokenData, text: Annotated[str, Body()]):
    # https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference
    response_data = await twitter_client.request(method='post', url='/tweets', auth_data=token_data, json={'text': text})
    return response_data['data']


'''
NOTE: unavailable in free tier

@router.post('/test/direct-message', response_model=dict)
async def send_direct_message(token_data: ReadTokenData, payload: SendDirectMessage):
    # https://developer.twitter.com/en/docs/twitter-api/direct-messages/manage/api-reference
    response_data = await twitter_client.request(method='post', url='/dm_conversations/with/:participant_id/messages', auth_data=token_data, json={'text': payload.message})
    return response_data
'''
