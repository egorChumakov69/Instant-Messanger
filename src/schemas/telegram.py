from pydantic import BaseModel


class SetTelegramIdSchema(BaseModel):
    token: str
    telegram_id: str | int
    chat_id: str | int
