from marshmallow import Schema, fields


class ThemeRequestSchema(Schema):
    title = fields.Str(required=True)


class ThemeResponseSchema(ThemeRequestSchema):
    id = fields.Int(required=False)


class ThemeListResponseSchema(Schema):
    themes = fields.Nested(ThemeResponseSchema, many=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionRequestSchema(Schema):
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(AnswerSchema, many=True)


class QuestionResponseSchema(QuestionRequestSchema):
    id = fields.Int(required=True)


class ThemeListSchema(Schema):
    pass


class ThemeIdSchema(Schema):
    pass


class QuestionListResponseSchema(Schema):
    questions = fields.Nested(QuestionResponseSchema, many=True)
