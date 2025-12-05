# DiggIndie-AI
DiggIndie AI (python) server repo
- python 3.12 가상환경에서 세팅했음
- 로컬에서 실행 시에
```commandline
python -m uvicorn app.main:app --reload --port 8000
```

- http://127.0.0.1:8000/health 링크 들어갔을 때 {"status":"ok"} 나와야 함

### 패키지 구조
```commandline
band-recommender-ai/
├─ app/
│  ├─ __init__.py
│  ├─ main.py          # FastAPI 엔트리포인트
│  ├─ db.py            # DB 연결/풀
│  ├─ schemas.py       # 요청/응답 Pydantic 모델
│  └─ services.py      # 임베딩 + 추천 로직
├─ .env.example        # 환경변수 예시
├─ requirements.txt
└─ README.md
```

++ 추가적으로, 그냥 ORM 안쓰고 SQL 문으로도 구현 가능할 것 같아서 우선 SQLAlchemy는 제외하고 세팅하였음