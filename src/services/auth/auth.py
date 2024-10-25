from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_sqlalchemy_session
from src.core.config import settings
from src.models.users.models import User
from src.models.tokens.models import RefreshToken
from src.services.auth.exceptions import (
    NotAuthorizedException,
    InvalidTokenException,
    TokenExpiredException
)
from src.services.auth.utils import (
    create_jwt_token,
    REFRESH_TYPE,
    ACCESS_TYPE,
    verify_password,
    decode_token
)
from src.services.users.service import UserService


async def create_access_token(data: dict, expire: Optional[datetime] = None) -> str:
    return create_jwt_token(data, ACCESS_TYPE, expire)


async def create_refresh_token(
    user: User,
    data: dict,
    expire: Optional[datetime] = None,
    db: AsyncSession = Depends(get_sqlalchemy_session)
) -> str:
    if not expire:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    token = create_jwt_token(data, REFRESH_TYPE, expire)
    await db.execute(delete(RefreshToken).where(RefreshToken.user_id == user.id))
    await db.commit()

    token_db = RefreshToken(
        user_id=user.id,
        token=token,
        expires_at=expire
    )
    db.add(token_db)
    await db.commit()
    await db.refresh(token_db)

    return token


async def authenticate_user(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    user = await UserService.get_user(db=db, username=username)
    if verify_password(password, user.password):
        return user
    raise NotAuthorizedException(detail='Invalid username or password')


async def token_refresh(
    refresh_token: str,
    db: AsyncSession = Depends(get_sqlalchemy_session)
) -> dict[str, str]:
    payload = decode_token(refresh_token)

    user_id: str = payload.get("sub")
    if user_id is None:
        raise InvalidTokenException()

    query = await db.execute(select(RefreshToken).filter_by(token=refresh_token))
    token: RefreshToken = query.scalars().first()

    if not token:
        raise InvalidTokenException

    if token.expires_at.replace(tzinfo=None) < datetime.utcnow():
        raise TokenExpiredException

    user = await UserService.get_user(db=db, id=int(user_id))

    token_data = {'sub': str(user.id)}

    access_token = await create_access_token(token_data)
    refresh_token = await create_refresh_token(user=user, data=token_data, db=db)

    return {'access_token': access_token, 'refresh_token': refresh_token}


async def get_user_from_token(
    token: str,
    db: AsyncSession = Depends(get_sqlalchemy_session)
) -> User:
    payload = decode_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise InvalidTokenException()
    user = await UserService.get_user(db=db, id=int(user_id))
    return user
