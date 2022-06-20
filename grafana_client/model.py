import dataclasses
from typing import Any, Dict, Optional


@dataclasses.dataclass
class DatasourceModel:
    name: str
    type: str
    url: str
    access: str
    database: Optional[str] = None
    user: Optional[str] = None
    jsonData: Optional[Dict] = None
    secureJsonData: Optional[Dict] = None
    secureJsonFields: Optional[Dict] = None

    def asdict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class DatasourceHealth:
    success: bool
    message: str
    duration: float
    response: Any

    def asdict(self):
        return dataclasses.asdict(self)

    def for_response(self):
        data = self.asdict()
        del data["response"]
        return data
