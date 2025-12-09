# app/db.py
import os
from typing import Any
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

from pgvector.psycopg2 import register_vector

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,   # 콘솔에 SQL 로그 보고 싶으면 True
)

@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    register_vector(dbapi_connection)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# if DATABASE_URL is None:
#     raise RuntimeError("DATABASE_URL is not set")


# # 간단한 커넥션 풀 설정 (추후 maxconn/minconn 조정 가능)
# pool = SimpleConnectionPool(
#     minconn=1,
#     maxconn=5,
#     dsn=DATABASE_URL,
# )


# def get_connection():
#     """
#     PostgreSQL 커넥션 풀에서 커넥션 하나 가져오기.
#     사용 후에는 반드시 release_connection()으로 반납해야 함.
#     """
#     conn = pool.getconn()
#     return conn


# def release_connection(conn: Any):
#     """
#     가져온 커넥션을 커넥션 풀에 반납.
#     """
#     if conn:
#         pool.putconn(conn)


# def close_all_connections():
#     """
#     애플리케이션 종료 시 호출해서 모든 커넥션 정리.
#     """
#     pool.closeall()
