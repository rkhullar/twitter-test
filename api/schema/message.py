from pydantic import BaseModel


class SendDirectMessage(BaseModel):
    username: str
    message: str
