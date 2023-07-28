import logging
from json.decoder import JSONDecodeError

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from httpx import HTTPStatusError
from starlette.middleware.sessions import SessionMiddleware

from .config import Settings
from .router import router as api_router

openapi_description = """
[login/twitter](/login/twitter)
"""


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        settings=settings,
        # swagger_ui_init_oauth={
        #     'clientId': settings.twitter_client_id,
        #     'usePkceWithAuthorizationCodeGrant': True,
        #     'scopes': ' '.join(settings.twitter_scopes)
        # }
        description=openapi_description
    )
    app.add_middleware(SessionMiddleware, secret_key=settings.authlib_secret)
    app.include_router(api_router)

    @app.exception_handler(HTTPStatusError)
    async def handle_http_status_error(request: Request, err: HTTPStatusError):
        logging.exception(err)
        error_data = {'status_code': err.response.status_code}
        try:
            error_data['detail'] = err.response.text
            error_data['detail'] = err.response.json()
        except JSONDecodeError:
            pass
        request = err.request
        request_context = {
            'method': request.method,
            'url': str(request.url),
            'headers': {key: value for key, value in request.headers.items()},
            'content': request.content.decode()
        }
        return JSONResponse(status_code=500, content={'error': error_data, 'request': request_context})

    return app
