import time

from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import SessionLocal
from app.models.band_description import BandDescription


BATCH_SIZE = 100  # 한 번에 몇 개씩 임베딩할지


def embed_missing_band_descriptions():
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    total_processed = 0

    while True:
        db: Session = SessionLocal()

        try:
            # 1) 아직 embedding이 없고, description은 있는 row만 가져오기
            rows = (
                db.query(BandDescription)
                .filter(
                    BandDescription.description.isnot(None),
                    BandDescription.embedding.is_(None),
                )
                .limit(BATCH_SIZE)
                .all()
            )

            if not rows:
                print("더 이상 처리할 데이터가 없습니다.")
                break

            texts = [row.description.strip() for row in rows]

            print(f"{len(rows)}개 행 임베딩 생성 중... (누적 {total_processed}개)")

            # 2) OpenAI 임베딩 API 한 번에 호출
            response = client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,  # text-embedding-3-small
                input=texts,
            )

            # 3) 응답을 각 row에 매핑해서 embedding 컬럼에 저장
            for row, item in zip(rows, response.data):
                row.embedding = item.embedding  # list[float] 바로 넣으면 됨

            db.commit()
            total_processed += len(rows)

        except Exception as e:
            db.rollback()
            print(f"에러 발생, 트랜잭션 롤백: {e}")
            # 필요하면 여기서 break 말고 continue 등으로 바꿔도 됨
            break
        finally:
            db.close()

        # API 과금/속도 고려해서 살짝 쉬고 싶으면
        time.sleep(0.2)

    print(f"전체 완료! 총 {total_processed}개 행 처리됨.")


if __name__ == "__main__":
    embed_missing_band_descriptions()
