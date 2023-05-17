from typing import Optional

from aiohttp.web_exceptions import HTTPConflict, HTTPUnprocessableEntity, HTTPNotFound
from aiohttp_apispec import querystring_schema, request_schema, response_schema

from app.quiz.models import Theme, Answer, Question
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        # get data
        title = self.data['title']
        theme: Optional[Theme] = await self.store.quizzes.get_theme_by_title(title=title)

        if theme is not None:
            raise HTTPConflict

        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        # get data
        themes: list[Theme] = await self.store.quizzes.list_themes()
        raw_themes = [ThemeSchema().dump(theme) for theme in themes]
        return json_response(data={'themes': raw_themes})


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        # get theme id
        theme_id: int = self.data['theme_id']
        theme: Optional[Theme] = await self.store.quizzes.get_theme_by_id(id_=theme_id)
        if theme is None:
            raise HTTPNotFound

        # get answers
        answers: list[Answer] = [
            Answer(
                title=data.get('title'), is_correct=data.get('is_correct')
            ) for data in self.data['answers']
        ]
        correct_answers = [answer for answer in answers if answer.is_correct]
        if len(answers) < 2 or len(correct_answers) != 1:
            raise HTTPUnprocessableEntity

        # get title
        title: str = self.data['title']
        question: Optional[Question] = await self.store.quizzes.get_question_by_title(title=title)
        if question is not None:
            raise HTTPConflict

        question = await self.store.quizzes.create_question(
            title=title, theme_id=theme_id, answers=answers
        )
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        # get data
        theme_id = self.data.get("theme_id")
        questions = await self.store.quizzes.list_questions(theme_id=theme_id)
        raw_questions = [QuestionSchema().dump(question) for question in questions]
        return json_response(data={'questions': raw_questions})
