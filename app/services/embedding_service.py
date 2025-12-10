import time
from typing import Tuple, List

from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import SessionLocal
from app.models.band_description import BandDescription


class EmbeddingService:

    def __init__(self) -> None:
        if not settings.has_openai_key:
            raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model_name = settings.OPENAI_EMBEDDING_MODEL

    # 단일 텍스트 임베딩 생성
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

    # 특정 band_description_id 배열에 대해서만 임베딩 생성/갱신
    def update_band_descriptions_by_ids(self, band_description_ids: List[int]) -> int:

        if not band_description_ids:
            raise ValueError("band_description_ids 리스트는 최소 1개 이상이어야 합니다.")

        batch_size = 100
        total_processed = 0

        db: Session = SessionLocal()

        try:
            # 대상 row 전부 조회 (description 이 있는 것만)
            rows: List[BandDescription] = (
                db.query(BandDescription)
                .filter(
                    BandDescription.band_description_id.in_(band_description_ids),
                    BandDescription.description.isnot(None),
                )
                .all()
            )

            if not rows:
                return 0

            # 배치 단위로 잘라서 임베딩 호출
            for i in range(0, len(rows), batch_size):
                batch_rows = rows[i : i + batch_size]
                texts = [row.description.strip() for row in batch_rows]

                # 공백 description 은 스킵
                valid_pairs = [
                    (row, text) for row, text in zip(batch_rows, texts) if text
                ]
                if not valid_pairs:
                    continue

                batch_rows_valid, texts_valid = zip(*valid_pairs)

                response = self.client.embeddings.create(
                    model=self.model_name,
                    input=list(texts_valid),
                )

                for row, item in zip(batch_rows_valid, response.data):
                    row.embedding = item.embedding

                total_processed += len(batch_rows_valid)

            db.commit()

            return total_processed

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    
    # 전체 임베딩 재생성
    def reset_band_descriptions_embedding(self) -> int:

        # 1) 모든 행의 embedding을 None 으로 초기화
        db: Session = SessionLocal()
        try:
            (
                db.query(BandDescription)
                .filter(BandDescription.description.isnot(None))
                .update({BandDescription.embedding: None}, synchronize_session=False)
            )
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"임베딩 초기화 중 에러 발생, 롤백: {e}")
            raise
        finally:
            db.close()

        # 2) 임베딩 업데이트 메소드 사용하여 임베딩 생성
        total_processed = self.update_missing_band_description_embedding()
        return total_processed


    # 임베딩이 없는 band_description에 대해 임베딩 수행
    def update_missing_band_description_embedding(self) -> int:

        batch_size = 100
        total_processed = 0

        while True:
            db: Session = SessionLocal()

            try:
                rows = (
                    db.query(BandDescription)
                    .filter(
                        BandDescription.description.isnot(None),
                        BandDescription.embedding.is_(None),
                    )
                    .limit(batch_size)
                    .all()
                )

                if not rows:
                    print("더 이상 처리할 데이터가 없습니다.")
                    break

                texts = [row.description.strip() for row in rows]

                print(f"{len(rows)}개 행 임베딩 생성 중... (누적 {total_processed}개)")

                response = self.client.embeddings.create(
                    model=self.model_name,
                    input=texts,
                )

                for row, item in zip(rows, response.data):
                    row.embedding = item.embedding

                db.commit()
                total_processed += len(rows)

            except Exception as e:
                db.rollback()
                print(f"에러 발생, 트랜잭션 롤백: {e}")
                break
            finally:
                db.close()

            time.sleep(0.2)

        print(f"임베딩 완료 : 총 {total_processed}개 행 처리됨.")
        return total_processed


embedding_service = EmbeddingService()
