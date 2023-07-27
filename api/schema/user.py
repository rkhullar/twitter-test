from pydantic import BaseModel
from typing import Literal


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
