import dataclasses
from typing import Any, Dict, Optional, Union


@dataclasses.dataclass
class DatasourceIdentifier:
    """
    A Grafana data source can be identified by either a numerical id, an
    alphanumerical uid, or a name.
    """

    id: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None


@dataclasses.dataclass
class DatasourceModel:
    """
    Represent the minimum required fields to create a JSON payload suitable for
    submitting to the Grafana HTTP API.

    TODO: Field `database` will be deprecated.
          https://github.com/grafana/grafana/issues/59115
    """

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
class DatasourceHealthResponse:
    """
    Represent a response for a Grafana data source health check.

    It is a mixture of the fields of the native, server-side health check
    introduced with Grafana 9+, and the client-side implementation by
    `grafana-client`.

    - Grafana 9+ uses the fields `status` and `message`, where `status` can be
      one of `OK`, or `ERROR`.
    - `grafana-client` employs a more verbose response, including metadata
      about the requested data source item (`uid`, `type`), a boolean `success`
      flag, as well as the duration in seconds the request needed and the full
      response object.
    """

    uid: str
    type: Union[str, None]
    success: bool
    status: str
    message: str
    duration: Optional[float] = None
    response: Optional[Any] = None

    def asdict(self):
        return dataclasses.asdict(self)

    def asdict_compact(self):
        data = self.asdict()
        del data["response"]
        return data


@dataclasses.dataclass
class PersonalPreferences:
    """
    Request/response model for user-, team- and organization-preferences.

    https://grafana.com/docs/grafana/latest/developers/http_api/preferences/
    """

    homeDashboardId: Optional[int] = None
    homeDashboardUID: Optional[str] = None
    locale: Optional[str] = None
    theme: Optional[str] = None
    timezone: Optional[str] = None
    weekStart: Optional[str] = None

    def asdict(self, filter_none=False):
        if filter_none:
            return dataclasses.asdict(self, dict_factory=self.dict_factory_filter_none)
        else:
            return dataclasses.asdict(self)

    @staticmethod
    def dict_factory_filter_none(seq=None, **kwargs):
        seq = [item for item in seq if item[1] is not None]
        data = dict(seq)
        data.update(kwargs)
        return data
