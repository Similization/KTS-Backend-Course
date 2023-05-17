from aiohttp_apispec import docs, request_schema, response_schema

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.schemes import OkResponseSchema


class AdminLoginView(View):
    @docs(tags=['admin'], summary='login', description='Try to login')
    # @request_schema(AdminSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        print(data)


class AdminCurrentView(View):
    @docs(tags=['admin'], summary='get', description='Get admin')
    @request_schema(AdminSchema)
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        raise NotImplementedError
