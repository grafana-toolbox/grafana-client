import requests
import requests.auth


class GrafanaException(Exception):
    def __init__(self, status_code, response, message):
        self.status_code = status_code
        self.response = response
        self.message = message
        # Backwards compatible with implementations that rely on just the message.
        super(GrafanaException, self).__init__(message)


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
        super(GrafanaBadInputError, self).__init__(
            400, response, "Bad Input: `{0}`".format(response)
        )


class GrafanaUnauthorizedError(GrafanaClientError):
    """
    401
    """

    def __init__(self, response):
        super(GrafanaUnauthorizedError, self).__init__(401, response, "Unauthorized")


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers.update({"Authorization": "Bearer {0}".format(self.token)})
        return request


class GrafanaAPI:
    def __init__(
        self,
        auth,
        host="localhost",
        port=None,
        url_path_prefix="",
        protocol="http",
        verify=True,
        timeout=5.0,
    ):
        self.auth = auth
        self.verify = verify
        self.timeout = timeout
        self.url_host = host
        self.url_port = port
        self.url_path_prefix = url_path_prefix
        self.url_protocol = protocol

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

        self.s = requests.Session()
        if not isinstance(self.auth, tuple):
            self.auth = TokenAuth(self.auth)
        else:
            self.auth = requests.auth.HTTPBasicAuth(*self.auth)

    def __getattr__(self, item):
        def __request_runnner(url, json=None, headers=None):
            __url = "%s%s" % (self.url, url)
            runner = getattr(self.s, item.lower())
            r = runner(
                __url,
                json=json,
                headers=headers,
                auth=self.auth,
                verify=self.verify,
                timeout=self.timeout,
            )
            if r.status_code >= 400:
                try:
                    response = r.json()
                except ValueError:
                    response = r.text
                message = response["message"] if "message" in response else r.text

                if 500 <= r.status_code < 600:
                    raise GrafanaServerError(
                        r.status_code,
                        response,
                        "Server Error {0}: {1}".format(r.status_code, message),
                    )
                elif r.status_code == 400:
                    raise GrafanaBadInputError(response)
                elif r.status_code == 401:
                    raise GrafanaUnauthorizedError(response)
                elif 400 <= r.status_code < 500:
                    raise GrafanaClientError(
                        r.status_code,
                        response,
                        "Client Error {0}: {1}".format(r.status_code, message),
                    )
            return r.json()

        return __request_runnner
