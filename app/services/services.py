# app/services.py
import os
from typing import List, Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# TODO:
# - 필요하면 OpenAI 클라이언트 옵션(타임아웃, 베이스 URL 등) 세분화
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def get_text_embedding(text: str) -> List[float]:
    """
    TODO:
    - OpenAI 임베딩 API를 호출해서 text를 벡터로 변환하는 로직 구현
    - 에러 처리 및 로깅 추가

    현재는 NotImplementedError만 던짐.
    """
    raise NotImplementedError("get_text_embedding() 로직을 구현하세요.")


def query_similar_bands(embedding: List[float], top_k: int = 5) -> List[Any]:
    """
    TODO:
    - db.get_connection()으로 커넥션 가져오기
    - pgvector <=> 연산자를 사용하여 bands 테이블에서 유사한 밴드 조회
    - rows: [(id, name, genre_desc, distance), ...] 형태로 반환하도록 구현

    현재는 NotImplementedError만 던짐.
    """
    raise NotImplementedError("query_similar_bands() 로직을 구현하세요.")


def recommend_bands(user_text: str, top_k: int = 5) -> List[Any]:
    """
    TODO:
    - 1) user_text → get_text_embedding()으로 임베딩 생성
    - 2) query_similar_bands() 호출
    - 3) 결과 rows를 그대로 반환하거나, 가공해서 리턴

    현재는 NotImplementedError만 던짐.
    """
    raise NotImplementedError("recommend_bands() 로직을 구현하세요.")
