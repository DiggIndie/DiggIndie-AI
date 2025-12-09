from fastapi import APIRouter, HTTPException

from app.schemas.embedding_schemas import (
    SingleEmbeddingRequest,
    SingleEmbeddingResponse,
)
from app.services.embedding_service import embedding_service

router = APIRouter(
    prefix="/embedding",
    tags=["embedding"],
)

@router.post("/single", response_model=SingleEmbeddingResponse)
async def create_single_embedding(body: SingleEmbeddingRequest):

    try:
        model, embedding = embedding_service.embed_single_text(body.text)
    except ValueError as ve:
        # 입력값 문제 
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # OpenAI 에러 또는 기타 예외
        raise HTTPException(status_code=500, detail=f"임베딩 생성 실패: {e}")

    return SingleEmbeddingResponse(
        model=model,
        embedding=embedding,
    )
