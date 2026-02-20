from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Literal

from sqlalchemy import DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column


Role = Literal["user", "assistant"]


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"
    __allow_unmapped__ = True  # ✅ Fix SQLAlchemy 2.0 annotation error

    id: int = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: str = mapped_column(String(128), index=True)
    role: str = mapped_column(String(16))
    text: str = mapped_column(Text)
    created_at: datetime = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class ChatTurn:
    role: Role
    text: str
    created_at: datetime


class HistoryStore:
    """
    Minimal persistent chat history store backed by SQLite.

    Notes:
    - DB path is provided via db_url, e.g. sqlite:///./chat_history.db
    - last_n() returns messages ordered oldest -> newest
    """

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url, future=True)
        Base.metadata.create_all(self.engine)

    def add(self, user_id: str, role: Role, text: str) -> None:
        user_id = (user_id or "").strip()
        text = (text or "").strip()
        if not user_id:
            raise ValueError("user_id is required")
        if not text:
            return  # silently skip empty content

        with Session(self.engine) as s:
            s.add(Message(user_id=user_id, role=role, text=text))
            s.commit()

    def last_n(self, user_id: str, n: int = 20) -> List[ChatTurn]:
        user_id = (user_id or "").strip()
        if not user_id:
            return []

        with Session(self.engine) as s:
            stmt = (
                select(Message)
                .where(Message.user_id == user_id)
                .order_by(Message.id.desc())
                .limit(int(n))
            )
            rows = list(s.execute(stmt).scalars())

        rows.reverse()  # oldest -> newest
        return [ChatTurn(role=row.role, text=row.text, created_at=row.created_at) for row in rows]

    def clear(self, user_id: str) -> None:
        user_id = (user_id or "").strip()
        if not user_id:
            return

        with Session(self.engine) as s:
            s.query(Message).filter(Message.user_id == user_id).delete()
            s.commit()