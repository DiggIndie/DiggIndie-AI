# DiggIndie-AI

벡터 기반 밴드 추천 시스템 - FastAPI 기반 AI 추천 서버

## 📌 프로젝트 개요

이 프로젝트는 **벡터 임베딩 기반의 밴드 추천 시스템**입니다. 사용자가 선택한 밴드와 키워드를 바탕으로, OpenAI 임베딩과 pgvector를 활용하여 유사한 밴드를 추천합니다.

### 핵심 기술 스택

- **FastAPI**: Python 기반 비동기 웹 프레임워크
- **PostgreSQL + pgvector**: 벡터 유사도 검색을 위한 확장
- **OpenAI Embeddings**: 텍스트를 1536차원 벡터로 변환 (text-embedding-3-small)
- **scikit-learn**: K-means 클러스터링을 통한 취향 그룹 분석
- **SQLAlchemy**: ORM을 통한 데이터베이스 접근

---

## 🚀 실행 방법

### 환경 설정

1. Python 3.12 가상환경 생성 및 활성화
2. 의존성 설치:
```bash
pip install -r requirements.txt
```

3. `.env` 파일 설정:
```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USERNAME=postgres
DB_PASSWORD=your_password

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# JWT
JWT_SECRET_KEY=your_base64_encoded_jwt_secret
```

### 서버 실행

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 헬스 체크

```bash
curl http://127.0.0.1:8000/health
# 응답: {"status":"ok"}
```

---

## 🎯 추천 알고리즘 (V3)

### API 엔드포인트

```
POST /api/bands/recommendations/update
```

**인증**: JWT Bearer Token 필요 (Authorization 헤더)

**반환**: 5개의 추천 밴드

### 동작 방식

최종 추천 API는 **V3 알고리즘**을 사용하여 사용자의 선호 밴드와 키워드를 기반으로 추천을 생성합니다.

#### 전체 흐름

```
1. JWT 토큰에서 사용자 정보 추출 (externalId)
   ↓
2. Member 테이블 조회 → memberId 획득
   ↓
3. MemberBand, MemberKeyword 조회 → bandIds, keywordIds 수집
   ↓
4. V3 추천 알고리즘 실행 (5개 반환)
   ↓
5. BandRecommend 테이블에 저장 (기존 데이터 삭제 후 새로 저장)
   ↓
6. Band + TopTrack + Keyword 정보와 함께 반환
```

#### V3 알고리즘 상세

**Step 1: 밴드 임베딩 조회**
- 사용자가 선택한 밴드들의 임베딩 벡터(1536차원)를 `band_description` 테이블에서 조회
- 각 밴드는 OpenAI로 생성된 임베딩 벡터를 보유

**Step 2: K-means 클러스터링 (k=3)**
- 선택된 밴드들을 **3개의 클러스터**로 분류
- 각 클러스터는 유사한 취향의 밴드 그룹을 나타냄
- `random_state=42`로 고정하여 동일한 입력에 대해 일관된 결과 보장

**Step 3: 키워드 임베딩 생성**
- 사용자가 선택한 키워드들을 문장으로 결합
- OpenAI API로 키워드 문장을 임베딩 벡터로 변환

**Step 4: 각 Centroid에 키워드 Slerp 적용**
- **Slerp (Spherical Linear Interpolation)**: 구면 선형 보간
- 각 클러스터의 중심점(centroid)에 키워드 벡터 방향을 반영
- **Adaptive t 계산**: 사용자 벡터와 키워드 벡터 간 유사도에 따라 키워드 영향력 동적 조절
  - 유사도 높음 → 적게 틀기 (t 작음)
  - 유사도 낮음 → 많이 틀기 (t 큼)

**Step 5: 각 클러스터별 상위 2개 밴드 검색**
- 조정된 각 centroid에서 **pgvector**를 활용하여 코사인 유사도가 높은 밴드 2개씩 검색
- 각 클러스터의 **1등 3개는 필수 포함** (다양성 확보)
- 각 클러스터의 **2등 3개 중 점수 높은 2개 추가** (품질 확보)
- 총 **5개 밴드 반환** (3 + 2)

**Step 6: 결과 저장 및 반환**
- 추천된 5개 밴드를 `band_recommend` 테이블에 저장
- `score` 높은 순으로 `priority` 1, 2, 3, 4, 5 부여
- Band, TopTrack, Keyword 정보와 함께 반환

### 알고리즘 특징

1. **다양성 확보**: 각 클러스터에서 1등씩 필수 포함 → 서로 다른 취향 그룹 반영
2. **품질 보장**: 2등 중 상위 2개 추가 → 높은 유사도의 추천 제공
3. **키워드 반영**: 모든 클러스터에 키워드 방향을 개별적으로 적용
4. **벡터 기반 유사도**: pgvector의 코사인 거리 연산자(`<=>`) 활용
5. **안정성**: 밴드가 3개 미만이면 자동으로 V2로 폴백

### 폴백 조건

- 밴드가 **3개 미만**이면 V2 알고리즘으로 자동 전환
- V2는 통합 사용자 벡터에 키워드를 Slerp로 적용하여 top 3 검색

---

## 📊 데이터베이스 구조

### 주요 테이블

- **band_description**: 밴드 설명 텍스트 + 임베딩 벡터 (pgvector)
- **band**: 밴드 기본 정보 (이름, 이미지, 대표곡 등)
- **keyword**: 키워드 마스터
- **band_keyword**: 밴드-키워드 연결
- **member**: 회원 정보
- **member_band**: 사용자가 선택한 밴드
- **member_keyword**: 사용자가 선택한 키워드
- **band_recommend**: 추천된 밴드 저장 (priority, score 포함)
- **top_track**: 밴드의 대표곡 정보

---

## 📁 프로젝트 구조

```
DiggIndie-AI/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 엔트리포인트
│   ├── core/
│   │   ├── config.py              # 설정 (DB, OpenAI, JWT)
│   │   ├── db.py                  # DB 연결 및 세션 관리
│   │   ├── auth.py                # JWT 인증 모듈
│   │   └── exceptions.py          # 커스텀 예외
│   ├── models/                    # SQLAlchemy 모델
│   │   ├── band.py
│   │   ├── band_description.py
│   │   ├── keyword.py
│   │   ├── member.py
│   │   ├── member_band.py
│   │   ├── member_keyword.py
│   │   ├── band_recommend.py
│   │   └── top_track.py
│   ├── repositories/              # 데이터베이스 접근 계층
│   │   └── band_description_repository.py
│   ├── services/                  # 비즈니스 로직
│   │   ├── recommendation_service.py  # V1, V2, V3 추천 알고리즘
│   │   └── embedding_service.py      # OpenAI 임베딩 생성
│   ├── schemas/                   # Pydantic 스키마
│   │   └── band_description_schemas.py
│   └── api/                       # API 라우트
│       ├── band_routes.py         # 밴드 추천 엔드포인트
│       └── embedding_routes.py    # 임베딩 생성 엔드포인트
├── .env                           # 환경변수 (gitignore)
├── requirements.txt
└── README.md
```

---

## 🔧 주요 기능

### 1. 밴드 추천 API (최종)

- **엔드포인트**: `POST /api/bands/recommendations/update`
- **인증**: JWT Bearer Token
- **동작**: 사용자의 선호 밴드/키워드를 기반으로 V3 알고리즘으로 추천 생성 및 저장

### 2. 추천 알고리즘 버전

- **V1**: 밴드 임베딩 평균 기반 (키워드 미사용, 3개 반환)
- **V2**: 밴드 + 키워드 Slerp 결합 (3개 반환)
- **V3**: 클러스터별 키워드 반영 (다양성 + 품질 확보, **5개 반환**) ⭐ **최종 API에서 사용**

### 3. 임베딩 관리

- 밴드 설명 텍스트를 OpenAI로 임베딩 생성
- pgvector를 활용한 벡터 유사도 검색

---

## 📝 API 응답 예시

```json
{
  "statusCode": 200,
  "isSuccess": true,
  "message": "추천 밴드 업데이트 API",
  "payload": {
    "bands": [
      {
        "bandId": 1387,
        "score": 0.6936,
        "bandName": "쏜애플",
        "imageUrl": "https://...",
        "topTrack": {
          "title": "멸종",
          "externalUrl": "https://spotify/..."
        },
        "keywords": ["열정", "몽환"]
      },
      {
        "bandId": 1103,
        "score": 0.6675,
        "bandName": "실리카겔",
        "imageUrl": "https://...",
        "topTrack": {
          "title": "NO PAIN",
          "externalUrl": "https://spotify/..."
        },
        "keywords": ["강렬한", "신나는"]
      },
      {
        "bandId": 962,
        "score": 0.6148,
        "bandName": "라쿠나",
        "imageUrl": "https://...",
        "topTrack": null,
        "keywords": ["감성", "서정"]
      },
      {
        "bandId": 754,
        "score": 0.6024,
        "bandName": "혁오",
        "imageUrl": "https://...",
        "topTrack": {
          "title": "Wi-ing Wi-ing",
          "externalUrl": "https://spotify/..."
        },
        "keywords": ["몽환", "독특한"]
      },
      {
        "bandId": 523,
        "score": 0.5887,
        "bandName": "검정치마",
        "imageUrl": "https://...",
        "topTrack": {
          "title": "EVERYTHING",
          "externalUrl": "https://spotify/..."
        },
        "keywords": ["감성", "잔잔한"]
      }
    ]
  }
}
```

---

## 🔐 인증

JWT 토큰을 `Authorization` 헤더에 포함하여 요청:

```
Authorization: Bearer {accessToken}
```

토큰에서 `externalId`를 추출하여 사용자 정보를 조회합니다.

---

## ⚠️ 에러 처리

- **401 Unauthorized**: 유효하지 않은 토큰
- **400 Bad Request**: 선택한 밴드/키워드가 없음
- **404 Not Found**: 회원을 찾을 수 없음

모든 에러는 다음 형식으로 반환됩니다:

```json
{
  "statusCode": 400,
  "message": "선택한 밴드가 없습니다."
}
```

---

## 🧪 기술 상세

### 벡터 임베딩

- **모델**: OpenAI `text-embedding-3-small`
- **차원**: 1536차원
- **저장**: PostgreSQL `pgvector` 확장의 `VECTOR(1536)` 타입

### 유사도 검색

- **연산자**: pgvector의 `<=>` (코사인 거리)
- **변환**: 코사인 유사도 = `1 - 코사인 거리`
- **범위**: -1 ~ 1 (1에 가까울수록 유사)

### 클러스터링

- **알고리즘**: K-means (k=3)
- **라이브러리**: scikit-learn
- **고정성**: `random_state=42`로 일관된 결과 보장

### Slerp (구면 선형 보간)

- 벡터의 의미적 강도를 유지하면서 방향 조정
- 단순 평균 대비 벡터 크기(norm) 보존
- 키워드 방향으로 자연스러운 회전

---

## 📚 참고 문서

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
