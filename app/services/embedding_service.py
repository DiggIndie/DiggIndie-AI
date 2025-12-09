from typing import Tuple
from openai import OpenAI

from app.core.config import settings


class EmbeddingService:
    def __init__(self) -> None:
        if not settings.has_openai_key:
            raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model_name = settings.OPENAI_EMBEDDING_MODEL

    def embed_single_text(self, text: str) -> Tuple[str, list[float]]:

        cleaned = text.strip()
        if not cleaned:
            raise ValueError("입력 text가 비어 있습니다.")

        response = self.client.embeddings.create(
            model=self.model_name,
            input=cleaned,
        )

        embedding = response.data[0].embedding
        return response.model, embedding

embedding_service = EmbeddingService()
