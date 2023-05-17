from typing import Optional

from aiohttp.web_exceptions import HTTPConflict, HTTPUnprocessableEntity, HTTPNotFound
from aiohttp_apispec import docs, request_schema, response_schema

from app.quiz.models import Theme, Question, Answer
from app.quiz.schemes import (
    ThemeRequestSchema,
    ThemeResponseSchema,
    ThemeListResponseSchema,
    QuestionRequestSchema,
    QuestionResponseSchema,
    QuestionListResponseSchema
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


# TODO: добавить проверку авторизации для этого View
class ThemeAddView(AuthRequiredMixin, View):
    # TODO: добавить валидацию с помощью aiohttp-apispec и marshmallow-схем
    @docs(tags=['theme'], summary='Add theme', description='Add theme in database')
    @request_schema(ThemeRequestSchema)
    @response_schema(ThemeResponseSchema, 200)
    async def post(self):
        await self.check_cookies(request=self.request)
        # title = (await self.request.json())["title]
        # TODO: заменить на self.data["title"] после внедрения валидации
        title = self.data['title']
        theme: Optional[Theme] = await self.store.quizzes.get_theme_by_title(title=title)

        # TODO: проверять, что не существует темы с таким же именем, отдавать 409 если существует
        if theme is not None:
            raise HTTPConflict

        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeResponseSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @docs(tags=['theme'], summary='Get theme list', description='Get theme list from database')
    @response_schema(ThemeListResponseSchema, 200)
    async def get(self):
        # check ability
        await self.check_cookies(request=self.request)

        themes: list[Theme] = await self.store.quizzes.list_themes()
        raw_themes = [ThemeResponseSchema().dump(theme) for theme in themes]
        return json_response(data={'themes': raw_themes})


class QuestionAddView(AuthRequiredMixin, View):
    @docs(tags=['question'], summary='Add question', description='Add question in database')
    @request_schema(QuestionRequestSchema)
    @response_schema(QuestionResponseSchema, 200)
    async def post(self):
        # check ability
        await self.check_cookies(request=self.request)

        title: str = self.data['title']

        theme_id: int = self.data['theme_id']
        theme: Optional[Theme] = await self.store.quizzes.get_theme_by_id(id_=theme_id)
        if theme is None:
            raise HTTPNotFound

        answers: list[dict] = self.data['answers']
        correct_answers = [
            Answer(
                title=answer.get('title'),
                is_correct=answer.get('is_correct')
            ) for answer in answers if answer.get('is_correct')
        ]
        if len(answers) < 2 or len(correct_answers) != 1:
            raise HTTPUnprocessableEntity

        question: Optional[Question] = await self.store.quizzes.get_question_by_title(title=title)
        if question is not None:
            raise HTTPConflict

        question = await self.store.quizzes.create_question(
            title=title, theme_id=theme_id, answers=answers
        )
        return json_response(data=QuestionResponseSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @docs(tags=['question'], summary='Get question list', description='Get question list from database')
    @response_schema(QuestionListResponseSchema, 200)
    async def get(self):
        # check ability
        await self.check_cookies(request=self.request)

        questions = await self.store.quizzes.list_questions()
        raw_questions = [QuestionResponseSchema().dump(question) for question in questions]
        return json_response(data={'questions': raw_questions})
