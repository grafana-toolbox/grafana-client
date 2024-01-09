from sys import modules

import niquests
import urllib3

modules["requests"] = niquests
modules["requests.adapters"] = niquests.adapters
modules["requests.exceptions"] = niquests.exceptions
modules["requests.packages.urllib3"] = urllib3

import requests_mock  # noqa: E402

__all__ = ("requests_mock",)
