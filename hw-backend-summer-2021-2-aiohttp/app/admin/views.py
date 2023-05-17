from hashlib import sha256
from typing import Optional

from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import new_session, get_session

from app.admin.models import Admin
from app.admin.schemes import (
    AdminRequestSchema,
    AdminResponseSchema
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @docs(
        tags=['admin'],
        summary='Authorize admin',
        description='Authorize admin and return information'
    )
    @request_schema(AdminRequestSchema)
    @response_schema(AdminResponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        hashed_password = sha256(data['password'].encode('utf-8')).hexdigest()
        admin: Optional[Admin] = await self.store.admins.get_by_email(email=data['email'])

        if admin is None or admin.password != hashed_password:
            raise HTTPForbidden

        session = await new_session(request=self.request)
        session['email'] = admin.email
        session['password'] = admin.password

        # return json_response(data={'admin_id': admin.id, 'password': admin.password})
        return json_response(data=AdminResponseSchema().dump(admin))


class AdminCurrentView(AuthRequiredMixin, View):
    @docs(tags=['admin'], summary='Get admin info', description='Get admin info from database')
    @response_schema(AdminResponseSchema, 200)
    async def get(self):
        admin = await self.check_cookies(request=self.request)
        return json_response(data={'admin_id': admin.id, 'password': admin.password})
