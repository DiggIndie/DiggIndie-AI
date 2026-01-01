from fastapi import APIRouter, HTTPException

from app.schemas.embedding_schemas import (
    SingleEmbeddingRequest,
    SingleEmbeddingResponse,
    BatchEmbeddingResponse,
    BulkIdsEmbeddingRequest,
    BulkIdsEmbeddingResponse,
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


@router.post("/reset", response_model=BatchEmbeddingResponse)
async def reset_band_descriptions_embedding():

    try:
        total = embedding_service.reset_band_descriptions_embedding()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"전체 임베딩 재생성 실패: {e}")

    return BatchEmbeddingResponse(
        mode="reset", 
        totalProcessed=total
    )


@router.post("/update-missing", response_model=BatchEmbeddingResponse)
async def update_missing_band_descriptions_embedding():

    try:
        total = embedding_service.update_missing_band_description_embedding()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"미임베딩 행 처리 실패: {e}")

    return BatchEmbeddingResponse(
        mode="update-missing", 
        totalProcessed=total
    )


@router.post("/update-by-ids", response_model=BulkIdsEmbeddingResponse)
async def update_embedding_by_ids(body: BulkIdsEmbeddingRequest):

    if not body.bandDescriptionIds:
        raise HTTPException(status_code=400, detail="bandDescriptionIds 는 최소 1개 이상이어야 합니다.")

    try:
        processed = embedding_service.update_band_descriptions_by_ids(
            band_description_ids=body.bandDescriptionIds
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"지정 id 임베딩 갱신 실패: {e}")

    return BulkIdsEmbeddingResponse(
        requestedCount=len(body.bandDescriptionIds),
        processedCount=processed,
    )
