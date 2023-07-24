import os

from pydantic_settings import BaseSettings


class ProjectSettings(BaseSettings):
    environment: str = os.environ['ENVIRONMENT']
    reload_fastapi: bool = 'RELOAD_FASTAPI' in os.environ


class NetworkSettings(BaseSettings):
    service_host: str = os.getenv('SERVICE_HOST', 'localhost')
    service_port: int = int(os.getenv('SERVICE_PORT', '8000'))


class TwitterSettings(BaseSettings):
    twitter_client_id: str = os.environ['TWITTER_CLIENT_ID']
    twitter_client_secret: str = os.environ['TWITTER_CLIENT_SECRET']
    twitter_scopes: list[str] = ['users.read', 'offline.access', 'tweet.read', 'tweet.write']


class Settings(ProjectSettings, NetworkSettings, TwitterSettings):
    pass
