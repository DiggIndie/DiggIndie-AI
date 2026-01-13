# app/core/auth.py
import logging
from typing import Optional

import jwt
from fastapi import Header

from app.core.config import settings
from app.core.exceptions import InvalidTokenException

logger = logging.getLogger(__name__)


def decode_jwt(token: str) -> dict:
    """
    JWT 토큰을 디코딩하여 payload를 반환합니다.
    
    Args:
        token: JWT 토큰 문자열
        
    Returns:
        디코딩된 payload (dict)
        
    Raises:
        InvalidTokenException: 토큰이 유효하지 않을 때
    """
    # 디버깅: JWT_SECRET 설정 확인
    jwt_secret = settings.JWT_SECRET
    if not jwt_secret:
        logger.error("JWT_SECRET이 설정되지 않았습니다. .env 파일을 확인하세요.")
        raise InvalidTokenException("서버 설정 오류: JWT_SECRET이 없습니다.")
    
    logger.debug(f"JWT_SECRET 길이: {len(jwt_secret)} bytes")
    
    try:
        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("만료된 JWT 토큰이 사용되었습니다.")
        raise InvalidTokenException("만료된 토큰입니다.")
    except jwt.InvalidTokenError as e:
        logger.warning(f"JWT 토큰 검증 실패: {e}")
        raise InvalidTokenException("유효하지 않은 토큰입니다.")


def get_external_id_from_token(token: str) -> str:
    """
    JWT 토큰에서 externalId(subject)를 추출합니다.
    
    Args:
        token: JWT 토큰 문자열
        
    Returns:
        externalId (str)
    """
    payload = decode_jwt(token)
    external_id = payload.get("sub")
    if not external_id:
        raise InvalidTokenException("토큰에 사용자 정보가 없습니다.")
    return external_id


def get_current_user_external_id(
    authorization: str = Header(..., description="Bearer {accessToken}")
) -> str:
    """
    Authorization 헤더에서 JWT 토큰을 추출하고 externalId를 반환합니다.
    FastAPI Depends에서 사용합니다.
    
    Args:
        authorization: Authorization 헤더 값 (Bearer {token} 형식)
        
    Returns:
        externalId (str)
        
    Raises:
        InvalidTokenException: 토큰이 없거나 유효하지 않을 때
    """
    if not authorization:
        raise InvalidTokenException("Authorization 헤더가 없습니다.")
    
    # Bearer 접두사 확인 및 제거
    if not authorization.startswith("Bearer "):
        raise InvalidTokenException("올바른 토큰 형식이 아닙니다. 'Bearer {token}' 형식을 사용하세요.")
    
    token = authorization[7:]  # "Bearer " 제거
    
    if not token:
        raise InvalidTokenException("토큰이 비어있습니다.")
    
    return get_external_id_from_token(token)
