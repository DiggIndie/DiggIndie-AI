# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.embedding_routes import router as embedding_router
from app.api.band_routes import router as band_router

from app.schemas.schemas import RecommendBandRequest, RecommendBandResponse, BandItem
from app.services.services import recommend_bands, EMBEDDING_MODEL

app = FastAPI(
    title="Band Recommender AI Service",
    description="사용자 음악 취향 텍스트 기반 밴드 추천 API",
    version="0.1.0",
)

app.include_router(embedding_router, prefix="/api")
app.include_router(band_router, prefix="/api")

# TODO:
# - 배포 환경에 맞게 allow_origins 수정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: 나중에 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

    # 구현 예시 (나중에 주석 해제해서 사용)
    # rows = recommend_bands(payload.user_text, top_k=payload.top_k)
    #
    # bands = [
    #     BandItem(
    #         id=row[0],
    #         name=row[1],
    #         genre_desc=row[2],
    #         distance=float(row[3]),
    #     )
    #     for row in rows
    # ]
    #
    # return RecommendBandResponse(
    #     model=EMBEDDING_MODEL,
    #     query_text=payload.user_text,
    #     bands=bands,
    # )
