from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2AuthorizationCodeBearer

router = APIRouter()

scopes = ['tweet.write']#, 'users:read']
auth_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl='https://twitter.com/i/oauth2/authorize',
    tokenUrl='https://api.twitter.com/2/oauth2/token',
    scopes={scope: scope for scope in scopes}
)


@router.get('/hello-world')
async def hello_world(token: str = Security(auth_scheme)):
    return dict(message='hello world', token=token)
