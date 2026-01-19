import os
import base64
from dotenv import load_dotenv

load_dotenv()  

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    @property
    def has_openai_key(self) -> bool:
        return bool(self.OPENAI_API_KEY)

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "postgres")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    
    # JWT 설정 (Spring과 동일한 BASE64 인코딩된 secret key)
    _JWT_SECRET_BASE64: str = os.getenv("JWT_SECRET_KEY", "")
    
    @property
    def JWT_SECRET(self) -> bytes:
        """BASE64로 인코딩된 JWT secret을 디코딩하여 반환"""
        if self._JWT_SECRET_BASE64:
            return base64.b64decode(self._JWT_SECRET_BASE64)
        return b""
    
    JWT_ALGORITHM: str = "HS256"
    
    # CORS 설정 (Spring Security와 동일한 기본값)
    # 환경 변수 CORS_ORIGINS로 오버라이드 가능 (쉼표로 구분)
    _CORS_ORIGINS_ENV: str = os.getenv("CORS_ORIGINS", "")
    
    # Spring Security와 동일한 기본 origins
    DEFAULT_CORS_ORIGINS: list[str] = [
        "https://diggindie.com",
        "https://api.diggindie.com",
        "https://www.diggindie.com",
        "http://localhost:3000",
        "http://localhost:8080",
        "https://digg-indie-fe.vercel.app",
    ]
    
    @property
    def CORS_ORIGINS_LIST(self) -> list[str]:
        """CORS origins를 리스트로 반환. 환경 변수가 있으면 사용, 없으면 기본값 사용"""
        if self._CORS_ORIGINS_ENV:
            if self._CORS_ORIGINS_ENV == "*":
                return ["*"]
            return [origin.strip() for origin in self._CORS_ORIGINS_ENV.split(",") if origin.strip()]
        return self.DEFAULT_CORS_ORIGINS

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()
