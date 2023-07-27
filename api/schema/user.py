from typing import Literal

from pydantic import BaseModel


class TwitterTokenData(BaseModel):
    token_type: Literal['bearer']
    expires_in: int
    access_token: str
    scope: str
    refresh_token: str
    expires_at: int

    @property
    def scopes(self) -> set[str]:
        return set(self.scope.split(' '))


class TwitterUserData(BaseModel):
    id: str  # NOTE: really an int but twitter returns as a string to avoid issues on the client
    name: str
    username: str
