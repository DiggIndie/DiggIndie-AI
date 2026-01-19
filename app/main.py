# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.embedding_routes import router as embedding_router
from app.api.band_routes import router as band_router
from app.core.config import settings

from app.schemas.schemas import RecommendBandRequest, RecommendBandResponse, BandItem
from app.services.services import recommend_bands, EMBEDDING_MODEL

import app.models  

app = FastAPI(
    title="Band Recommender AI Service",
    description="사용자 음악 취향 텍스트 기반 밴드 추천 API",
    version="0.1.0",
)

app.include_router(embedding_router, prefix="/api")
app.include_router(band_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,  
)

@app.get("/health")
def health_check():
    """
    헬스 체크 엔드포인트.
    필요하면 DB 접속 테스트 로직도 여기에 추가 가능.

    TODO:
    - db.get_connection() 시도해서 DB 상태도 같이 체크하도록 확장 가능
    """
    return {"status": "ok"}


@app.post("/recommend/band", response_model=RecommendBandResponse)
def recommend_band(payload: RecommendBandRequest):
    """
    Spring 서버에서 호출할 엔드포인트.

    TODO:
    - services.recommend_bands() 구현 후 실제 추천 결과 반환
    - 예외 처리, 로깅, 시간 측정 등 추가

    지금은 501 Not Implemented를 던지도록 해둠.
    """
    raise HTTPException(status_code=501, detail="Band recommendation not implemented yet.")
