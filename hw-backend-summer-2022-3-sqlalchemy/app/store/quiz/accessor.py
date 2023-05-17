from aiohttp.web import (
    HTTPBadRequest
)
from sqlalchemy import select, text, insert
from sqlalchemy.orm import joinedload, defaultload
from sqlalchemy.engine.result import ChunkedIteratorResult

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme,
    ThemeModel,
    QuestionModel, AnswerModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        query = insert(ThemeModel).values(title=title).returning(ThemeModel)
        async with self.app.database.session.begin() as session:
            res: ChunkedIteratorResult = await session.execute(query)
            theme_id = res.scalar()
            await session.commit()
            return Theme(id=theme_id, title=title)

    async def get_theme_by_title(self, title: str) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.title == title)
        async with self.app.database.session.begin() as session:
            res: ChunkedIteratorResult = await session.execute(query)
            theme_model: ThemeModel = res.scalar()
            if theme_model:
                return Theme(id=theme_model.id, title=theme_model.title)
            return None

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.id == id_)
        async with self.app.database.session.begin() as session:
            res: ChunkedIteratorResult = await session.execute(query)
            theme_model: ThemeModel = res.scalar()
            if theme_model:
                return Theme(id=theme_model.id, title=theme_model.title)
            return None

    async def list_themes(self) -> list[Theme]:
        query = select(ThemeModel)
        async with self.app.database.session.begin() as session:
            res: ChunkedIteratorResult = await session.execute(query)
            theme_models: list[ThemeModel] = res.scalars()
            return [Theme(id=theme_model.id, title=theme_model.title) for theme_model in theme_models]

    async def create_answers(
            self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        answer_list = [
            vars(AnswerModel(
                question_id=question_id,
                title=answer.title,
                is_correct=answer.is_correct
            )) for answer in answers
        ]
        query_get = select(AnswerModel).where(AnswerModel.question_id == question_id)
        async with self.app.database.session.begin() as session:
            await session.execute(
                insert(AnswerModel),
                answer_list
            )

            res: ChunkedIteratorResult = await session.execute(query_get)
            answer_models: list[AnswerModel] = res.scalars().all()

            await session.commit()
            return [
                Answer(
                    title=answer_model.title,
                    is_correct=answer_model.is_correct
                ) for answer_model in answer_models
            ]

    async def create_question(
            self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        correct_answers = [answer for answer in answers if answer.is_correct]
        if len(answers) < 2 or len(correct_answers) != 1:
            raise HTTPBadRequest

        query_add = insert(QuestionModel) \
            .values(title=title, theme_id=theme_id) \
            .returning(QuestionModel)
        async with self.app.database.session.begin() as session:

            # add question
            res: ChunkedIteratorResult = await session.execute(query_add)
            question_id = res.scalar()
            await session.commit()

        # add answers
        await self.create_answers(answers=answers, question_id=question_id)

        return Question(id=question_id, title=title, theme_id=theme_id, answers=answers)

    async def get_question_by_title(self, title: str) -> Question | None:
        query_get = select(QuestionModel)\
            .options(joinedload('answers'))\
            .where(QuestionModel.title == title)
        async with self.app.database.session.begin() as session:
            res: ChunkedIteratorResult = await session.execute(query_get)
            question_model: QuestionModel = res.scalar()
        if question_model is None:
            return None
        answers: list[Answer] = [
            Answer(
                title=answer.title, is_correct=answer.is_correct
            ) for answer in question_model.answers
        ]
        return Question(
            id=question_model.id,
            title=title,
            theme_id=question_model.theme_id,
            answers=answers
        )

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        query_get = select(QuestionModel).options(joinedload('answers'))
        if theme_id:
            query_get = query_get.where(QuestionModel.theme_id == theme_id)
        async with self.app.database.session.begin() as session:
            res: ChunkedIteratorResult = await session.execute(query_get)
            question_models: list[QuestionModel] = res.scalars().unique().all()

        result: list[Question] = []
        for question_model in question_models:
            answers: list[Answer] = [
                Answer(
                    title=answer.title, is_correct=answer.is_correct
                ) for answer in question_model.answers
            ]
            result.append(Question(
                id=question_model.id,
                title=question_model.title,
                theme_id=question_model.theme_id,
                answers=answers
            ))
        return result
