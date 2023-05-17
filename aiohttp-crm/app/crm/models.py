from dataclasses import dataclass
import uuid


@dataclass
class User:
    id_: uuid.UUID
    email: str
