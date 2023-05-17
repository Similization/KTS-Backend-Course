from typing import Optional

from aiohttp_session import get_session
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden

from app.admin.models import Admin


class AuthRequiredMixin:
    # TODO: можно использовать эту mixin-заготовку для реализации проверки авторизации во View

    @staticmethod
    async def check_cookies(request) -> Admin:
        session = await get_session(request)
        if session.new:
            raise HTTPUnauthorized
        admin: Optional[Admin] = await request.app.store.admins.get_by_email(email=session['email'])
        if admin.password != session.get('password'):
            raise HTTPForbidden
        return admin
