from fastapi import FastAPI

from .config import Settings
from .router import router as api_router

from starlette.middleware.sessions import SessionMiddleware


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        settings=settings,
        # swagger_ui_init_oauth={
        #     'clientId': settings.twitter_client_id,
        #     'usePkceWithAuthorizationCodeGrant': True,
        #     'scopes': ' '.join(settings.twitter_scopes)
        # }
    )
    app.add_middleware(SessionMiddleware, secret_key=settings.authlib_secret)
    app.include_router(api_router)
    return app
