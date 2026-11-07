"""Reproduce #535 on Postgres with miminet's session-selection queries.

Scenario from the issue: task 7 solved, then user works on another task and
task 7 flips to 0/1. Steps:
  1. session A for section 7: finished, 1/1 correct
  2. session B for section 7: started (user reopened task 7), never answered
  3. user clicks "start" on section 8 -> front calls finish_old_sessions(),
     which stamps finished_at=now() on every unfinished session (incl. B)
"""

import os
import time

from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class QuizSession(Base):
    __tablename__ = "quiz_session"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_by_id: Mapped[int] = mapped_column(BigInteger)
    section_id: Mapped[int] = mapped_column(BigInteger)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_on = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    finished_at = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    sessions = relationship("SessionQuestion")


class SessionQuestion(Base):
    __tablename__ = "session_question"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    quiz_session_id: Mapped[int] = mapped_column(ForeignKey("quiz_session.id"))
    is_correct = mapped_column(Boolean, nullable=True)


def correct(s):
    return sum(1 for q in s.sessions if q.is_correct)


def last_as_in_main(db, section_id, nulls_last=False):
    order = QuizSession.finished_at.desc()
    if nulls_last:
        order = order.nulls_last()
    q = (
        select(QuizSession)
        .where(QuizSession.created_by_id == 1, QuizSession.section_id == section_id)
        .order_by(order)
    )
    s = db.scalars(q).first()
    return f"session {s.id} -> {correct(s)}/1"


def best_finished(db, section_id):
    q = select(QuizSession).where(
        QuizSession.created_by_id == 1,
        QuizSession.section_id == section_id,
        QuizSession.is_deleted.is_(False),
        QuizSession.finished_at.isnot(None),
    )
    return f"best -> {max(correct(s) for s in db.scalars(q))}/1"


engine = create_engine(os.environ["DB_URL"])
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as db:
    a = QuizSession(id=1, created_by_id=1, section_id=7)
    a.sessions = [SessionQuestion(id=1, is_correct=True)]
    db.add(a)
    db.commit()
    a.finished_at = func.now()
    db.commit()
    print("after solving task 7:          ", last_as_in_main(db, 7))

    time.sleep(1)
    b = QuizSession(id=2, created_by_id=1, section_id=7)
    b.sessions = [SessionQuestion(id=2, is_correct=None)]
    db.add(b)
    db.commit()
    print("task 7 reopened, not answered:  ", last_as_in_main(db, 7),
          "| nulls_last:", last_as_in_main(db, 7, nulls_last=True))

    # finish_old_sessions(): every unfinished session of the user gets now()
    time.sleep(1)
    for s in db.scalars(select(QuizSession).where(QuizSession.finished_at.is_(None))):
        s.finished_at = func.now()
    db.commit()
    print("after starting task 8:          ", last_as_in_main(db, 7),
          "| nulls_last:", last_as_in_main(db, 7, nulls_last=True),
          "|", best_finished(db, 7))
