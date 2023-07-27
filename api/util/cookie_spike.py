from fastapi.openapi.models import APIKeyIn, SecuritySchemeType
from fastapi.security.base import SecurityBase, SecurityBaseModel
from pydantic import Field
from starlette.requests import Request


class CookieAuthModel(SecurityBaseModel):
    type_: SecuritySchemeType = Field(default=SecuritySchemeType.http, alias='type')
    in_: APIKeyIn = Field(default=APIKeyIn.cookie, alias='in')


class CookieAuth(SecurityBase):
    def __init__(self):
        self.scheme_name = self.__class__.__name__
        self.model = CookieAuthModel()

    async def __call__(self, request: Request) -> str | None:
        print('inside call')
        print(request.headers)
        print(request.session)
        return 'test'


'''
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None  # pragma: nocover
        return param
'''
