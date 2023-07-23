from fastapi import FastAPI

from .config import Settings
from .router import router as api_router


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        settings=settings,
        swagger_ui_init_oauth={
            'clientId': settings.twitter_client_id,
            'clientSecret': settings.twitter_client_secret,
            'usePkceWithAuthorizationCodeGrant': True,
            'scopes': ' '.join(['tweet.write']) # users:read
        }
    )
    app.include_router(api_router)
    return app