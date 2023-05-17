import typing
from hashlib import sha256
from typing import Optional

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        # TODO: создать админа по данным в config.yml здесь
        admin = app.config.admin
        hashed_password = sha256(admin.password.encode('utf-8')).hexdigest()
        app.database.admins.append(Admin(id=1, email=admin.email, password=hashed_password))
        # app.database.admins.append(Admin(id=1, email=admin.email, password=admin.password))

    async def get_by_email(self, email: str) -> Optional[Admin]:
        for admin in self.app.database.admins:
            if admin.email == email:
                return admin
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        hashed_password = sha256(password.encode('utf-8')).hexdigest()
        admin = Admin(id=self.app.database.next_admin_id, email=email, password=hashed_password)
        self.app.database.admins.append(admin)
        return admin
