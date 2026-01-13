# app/core/exceptions.py
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


class CustomHTTPException(HTTPException):
    """커스텀 에러 응답 형식을 위한 기본 클래스"""
    def __init__(self, status_code: int, message: str):
        super().__init__(
            status_code=status_code,
            detail={"statusCode": status_code, "message": message}
        )


class NoBandSelectedException(CustomHTTPException):
    """선택한 밴드가 없을 때 발생하는 예외"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="선택한 밴드가 없습니다."
        )


class NoKeywordSelectedException(CustomHTTPException):
    """선택한 키워드가 없을 때 발생하는 예외"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="선택한 키워드가 없습니다."
        )


class MemberNotFoundException(CustomHTTPException):
    """회원을 찾을 수 없을 때 발생하는 예외"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="회원을 찾을 수 없습니다."
        )


class InvalidTokenException(HTTPException):
    """토큰이 유효하지 않을 때 발생하는 예외"""
    def __init__(self, message: str = "유효하지 않은 토큰입니다."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"statusCode": status.HTTP_401_UNAUTHORIZED, "message": message},
            headers={"WWW-Authenticate": "Bearer"}
        )
