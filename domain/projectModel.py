from dataclasses import dataclass
from dataclasses import field
from domain.model import Model


@dataclass
class Project(Model):
    id: int = None
    name: str = None
    creator: str = None
    disabled: int = 0
    deleted: int = 0
    create_time: str = field(default=None)
    update_time: str = field(default=None)
