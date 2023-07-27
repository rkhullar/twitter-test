from fastapi import HTTPException, status, Security
from starlette.requests import Request
from typing import Annotated
from .schema.user import TwitterTokenData


async def read_token_data(request: Request) -> TwitterTokenData:
    if not request.session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return TwitterTokenData(**request.session)


ReadTokenData = Annotated[TwitterTokenData, Security(read_token_data)]


async def read_access_token(token_data: ReadTokenData) -> str:
    # TODO: inspect current time; try to refresh if expired?
    return token_data.access_token

ReadAccessToken = Annotated[str, Security(read_access_token)]
