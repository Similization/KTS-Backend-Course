from dataclasses import dataclass

from sqlalchemy import (
    Integer,
    VARCHAR,
    Column,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: int | None
    title: str


@dataclass
class Question:
    id: int | None
    title: str
    theme_id: int
    answers: list["Answer"]


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(VARCHAR(120), unique=True, nullable=False)

    question: "QuestionModel" = relationship("QuestionModel", cascade="all,delete", backref="themes")


class QuestionModel(db):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(VARCHAR(120), unique=True, nullable=False)
    theme_id = Column(Integer, ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)

    answers: list["AnswerModel"] = relationship("AnswerModel", cascade="all,delete", backref="questions")


class AnswerModel(db):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # var 1
    question_id = Column(Integer, ForeignKey(
        "questions.id", ondelete="CASCADE"
    ), nullable=False)
    title = Column(VARCHAR(120), nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)

# var 2
# class QuestionAnswersModel(db):
#     __tablename__ = "question_answers"
#
#     id = Column(Integer, primary_key=True)
#     question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)
#     answer_id = Column(Integer, ForeignKey("answers.answer_id"), nullable=False)
