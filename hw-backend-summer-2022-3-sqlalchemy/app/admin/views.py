from typing import Optional

from aiohttp.web import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from app.admin.models import Admin
from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        # get data
        data = self.request["data"]
        # get admin by email from data
        admin: Optional[Admin] = await self.store.admins.get_by_email(data["email"])
        # check conditions
        if admin is None or not admin.is_password_valid(data["password"]):
            raise HTTPForbidden

        session = await new_session(request=self.request)
        session["admin"] = {
            "id": admin.id,
            "email": admin.email
        }

        return json_response(data=AdminSchema().dump(admin))


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        admin = self.request.admin
        if admin is None:
            raise HTTPUnauthorized
        return json_response(data=AdminSchema().dump(admin))
