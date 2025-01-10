import niquests
import niquests.auth
from niquests import HTTPError, Timeout
from niquests.exceptions import JSONDecodeError

DEFAULT_TIMEOUT: float = 5.0
DEFAULT_SESSION_POOL_SIZE: int = 10


class GrafanaException(Exception):
    def __init__(self, status_code, response, message):
        self.status_code = status_code
        self.response = response
        self.message = message
        # Backwards compatible with implementations that rely on just the message.
        super(GrafanaException, self).__init__(message)


class GrafanaTimeoutError(GrafanaException):
    """
    A timeout occurred
    """


class GrafanaServerError(GrafanaException):
    """
    5xx
    """

    pass


class GrafanaClientError(GrafanaException):
    """
    Invalid input (4xx errors)
    """

    pass


class GrafanaBadInputError(GrafanaClientError):
    """
    400
    """

    def __init__(self, response):
        super(GrafanaBadInputError, self).__init__(400, response, f"Bad Input: `{response}`")


class GrafanaUnauthorizedError(GrafanaClientError):
    """
    401
    """

    def __init__(self, response):
        super(GrafanaUnauthorizedError, self).__init__(401, response, "Unauthorized")


class TokenAuth(niquests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers.update({"Authorization": f"Bearer {self.token}"})
        return request


class HeaderAuth(niquests.auth.AuthBase):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __call__(self, request):
        request.headers.update({self.name: self.value})
        return request


class GrafanaClient:
    def __init__(
        self,
        auth,
        host="localhost",
        port=None,
        url_path_prefix="",
        protocol="http",
        verify=True,
        timeout=DEFAULT_TIMEOUT,
        user_agent: str = None,
        organization_id: int = None,
        session_pool_size=DEFAULT_SESSION_POOL_SIZE,
    ):
        self.auth = auth
        self.verify = verify
        self.timeout = timeout
        self.url_host = host
        self.url_port = port
        self.url_path_prefix = url_path_prefix
        self.url_protocol = protocol
        self.session_pool_size = session_pool_size

        def construct_api_url():
            params = {
                "protocol": self.url_protocol,
                "host": self.url_host,
                "url_path_prefix": self.url_path_prefix,
            }

            if self.url_port is None:
                url_pattern = "{protocol}://{host}/{url_path_prefix}api"
            else:
                params["port"] = self.url_port
                url_pattern = "{protocol}://{host}:{port}/{url_path_prefix}api"

            return url_pattern.format(**params)

        self.url = construct_api_url()

        from grafana_client import __appname__, __version__

        self.user_agent = user_agent or f"{__appname__}/{__version__}"

        self.s = niquests.Session(pool_maxsize=session_pool_size)
        self.s.headers["User-Agent"] = self.user_agent

        self.organization_id = organization_id
        if self.organization_id:
            # orgId is defined in the openapi3 spec as an int64, but headers need to be a str
            self.s.headers["X-Grafana-Org-Id"] = str(self.organization_id)

        if self.auth is not None:
            if isinstance(self.auth, niquests.auth.AuthBase):
                pass
            elif isinstance(self.auth, tuple):
                self.auth = niquests.auth.HTTPBasicAuth(*self.auth)
            else:
                self.auth = TokenAuth(self.auth)

    def _make_url(self, url):
        return f"{self.url}{url}"

    @staticmethod
    def _ensure_valid_json_arg(json):
        if json is not None and not isinstance(json, (dict, list)):
            raise TypeError(
                f"JSON request payload has invalid shape. "
                f"Accepted are dictionaries and lists. "
                f"The type is: {type(json)}"
            )

    @staticmethod
    def _extract_from_response(r, accept_empty_json):
        if r.status_code >= 400:
            try:
                response = r.json()
            except ValueError:
                response = r.text
            message = response["message"] if isinstance(response, dict) and "message" in response else r.text

            if 500 <= r.status_code < 600:
                raise GrafanaServerError(
                    r.status_code,
                    response,
                    f"Server Error {r.status_code}: {message}",
                )
            elif r.status_code == 400:
                raise GrafanaBadInputError(response)
            elif r.status_code == 401:
                raise GrafanaUnauthorizedError(response)
            elif 400 <= r.status_code < 500:
                raise GrafanaClientError(
                    r.status_code,
                    response,
                    f"Client Error {r.status_code}: {message}",
                )

        # `204 No Content` responses have an empty response body,
        # so it doesn't decode well from JSON.
        if r.status_code == 204:
            return None

        # The "Tempo" data source responds with text/plain.
        content_type = r.headers.get("Content-Type", "")
        if content_type.startswith("text/"):
            return r.text
        try:
            return r.json()
        except JSONDecodeError:
            if accept_empty_json and r.text == "":
                return ""
            else:
                raise

    def __getattr__(self, item):
        def __request_runner(url, json=None, data=None, params=None, headers=None, accept_empty_json=False):
            __url = self._make_url(url)
            # Sanity checks.
            self._ensure_valid_json_arg(json)

            try:
                r = self.s.request(
                    item.lower(),
                    __url,
                    json=json,
                    data=data,
                    params=params,
                    headers=headers,
                    auth=self.auth,
                    verify=self.verify,
                    timeout=self.timeout,
                )
            except Timeout as e:
                raise GrafanaTimeoutError(0, None, str(e)) from e
            except HTTPError as e:
                # Make sure to not leak any exception types of the requests implementation.
                raise GrafanaException(0, None, str(e)) from e

            return self._extract_from_response(r, accept_empty_json)

        return __request_runner


class AsyncGrafanaClient(GrafanaClient):
    def __init__(
        self,
        auth,
        host="localhost",
        port=None,
        url_path_prefix="",
        protocol="http",
        verify=True,
        timeout=DEFAULT_TIMEOUT,
        user_agent: str = None,
        organization_id: int = None,
        session_pool_size=DEFAULT_SESSION_POOL_SIZE,
    ):
        super().__init__(
            auth,
            host=host,
            port=port,
            url_path_prefix=url_path_prefix,
            protocol=protocol,
            verify=verify,
            timeout=timeout,
            user_agent=user_agent,
            organization_id=organization_id,
            session_pool_size=session_pool_size,
        )
        self.s = niquests.AsyncSession(pool_maxsize=session_pool_size)
        self.s.headers.setdefault("Connection", "keep-alive")

    def __getattr__(self, item):
        async def __request_runner(url, json=None, data=None, params=None, headers=None, accept_empty_json=False):
            __url = self._make_url(url)
            # Sanity checks.
            self._ensure_valid_json_arg(json)

            try:
                r = await self.s.request(
                    item.lower(),
                    __url,
                    json=json,
                    data=data,
                    params=params,
                    headers=headers,
                    auth=self.auth,
                    verify=self.verify,
                    timeout=self.timeout,
                )
            except Timeout as e:
                raise GrafanaTimeoutError(0, None, str(e)) from e
            except HTTPError as e:
                raise GrafanaException(0, None, str(e)) from e

            return self._extract_from_response(r, accept_empty_json)

        return __request_runner
