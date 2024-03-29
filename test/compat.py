from sys import modules

import niquests
import urllib3

modules["requests"] = niquests
modules["requests.adapters"] = niquests.adapters
modules["requests.exceptions"] = niquests.exceptions
modules["requests.packages.urllib3"] = urllib3

import requests_mock  # noqa: E402


class Mocker(requests_mock.Mocker):
    """
    This monkeypatch class aim to fix a bug in "requests_mock"
    The library does not add "application/json" header in the response mock,
    when it's clearly about a json response. Niquests does not like it and require
    (as per RFC) a proper content type header to proceed.
    """

    def request(self, *args, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        if "json" in kwargs and kwargs["json"] is not None:
            kwargs["headers"]["Content-Type"] = "application/json"
        return self.register_uri(*args, **kwargs)


setattr(requests_mock, "Mocker", Mocker)

__all__ = ("requests_mock",)
