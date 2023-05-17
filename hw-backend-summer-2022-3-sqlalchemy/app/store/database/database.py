from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.store.database import db

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(
            "postgresql+asyncpg://postgres:mysecretpassword@localhost/kts",
            echo=True,
            future=True
        )
        self.session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )
        await self.app.store.admins.create_admin(
            email=self.app.config.admin.email,
            password=self.app.config.admin.password
        )

    async def disconnect(self, *_: list, **__: dict) -> None:
        # if self.session is not None:
        #     await self.session
        if self._engine is not None:
            await self._engine.dispose()
