from dataclasses import dataclass

from httpx import AsyncClient

from .schema.user import TwitterTokenData
from .util import BearerAuth


@dataclass(frozen=True)
class TwitterAPIClient:

    @property
    def base_url(self) -> str:
        return 'https://api.twitter.com/2'

    async def request(self, auth_data: TwitterTokenData, **kwargs) -> dict:
        client = AsyncClient(base_url=self.base_url, auth=BearerAuth(auth_data.access_token))
        response = await client.request(**kwargs)
        response.raise_for_status()
        return response.json()
