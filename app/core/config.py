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

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()
