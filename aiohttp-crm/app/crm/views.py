import uuid

from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden
from aiohttp_apispec import docs, request_schema, \
    response_schema, querystring_schema

from app.crm.models import User
from app.crm.schemes import UserAddSchema, ListUsersResponseSchema, \
    UserGetRequestSchema, UserGetResponseSchema, UserSchema
from app.web.app import View
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response, check_basic_auth


class AddUserView(View):
    @docs(tags=['crm'], summary='Add new user', description='Add new user to database')
    @request_schema(UserAddSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        user = User(email=data['email'], id_=uuid.uuid4())
        await self.request.app.crm_accessor.add_user(user=user)
        return json_response()


class ListUserView(View):
    @docs(tags=['crm'], summary='List of users', description='List of users from database')
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get('Authorization'):
            raise HTTPUnauthorized
        if not check_basic_auth(raw_credentials=self.request.headers['Authorization'],
                                username=self.request.app.config.username,
                                password=self.request.app.config.password):
            raise HTTPForbidden
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [UserSchema().dump(user) for user in users]
        return json_response(data={'users': raw_users})


class GetUserView(View):
    @docs(tags=['crm'], summary='Get user', description='Get user from database')
    @querystring_schema(UserGetRequestSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get('Authorization'):
            raise HTTPUnauthorized
        if not check_basic_auth(
                raw_credentials=self.request.headers['Authorization'],
                username=self.request.app.config.username,
                password=self.request.app.config.password
        ):
            raise HTTPForbidden
        user_id = self.request.query['id']
        try:
            user_id = _id = uuid.UUID(user_id)
        except ValueError:
            return json_response(status='bad id')

        user = await self.request.app.crm_accessor.get_user(_id=user_id)

        if user:
            return json_response(data={'user': UserSchema().dump(user)})
        return json_response(status='user does not exist')
