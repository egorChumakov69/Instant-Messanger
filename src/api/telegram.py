from urllib.parse import quote

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.database import get_sqlalchemy_session
from src.models.users.models import User
from src.schemas.telegram import SetTelegramIdSchema
from src.services.telegram.service import TelegramService
from src.services.users.dependencies import get_current_user

router = APIRouter(prefix='/telegram', tags=['telegram'])


@router.get('/get_token')
async def get_telegram_link_token(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    token = await TelegramService.set_telegram_link_token(user=current_user, db=db)
    response = f'https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={quote(token)}'
    return response


@router.post('/set_telegram_id')
async def set_telegram_id(
    request: SetTelegramIdSchema,
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    response = await TelegramService.set_user_telegram_id(
        token=request.token,
        telegram_id=request.telegram_id,
        chat_id=request.chat_id,
        db=db
    )
    return response


@router.post('/auth')
async def telegram_bot_auth(
    telegram_id: str | int,
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    response = await TelegramService.get_telegram_access_token(telegram_id, db=db)
    return response
