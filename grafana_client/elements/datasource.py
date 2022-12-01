import json
import logging
import time
import warnings
from distutils.version import LooseVersion
from typing import Dict, Optional, Tuple, Union

from requests import ReadTimeout

from ..client import GrafanaBadInputError, GrafanaClientError, GrafanaServerError
from ..knowledge import get_healthcheck_expression, query_factory
from ..model import DatasourceHealthResponse, DatasourceIdentifier
from .base import Base

logger = logging.getLogger(__name__)

VERSION_9 = LooseVersion("9")
VERBOSE = False


class Datasource(Base):
    def __init__(self, client, api):
        super(Datasource, self).__init__(client)
        self.client = client
        self.api = api

    def health(self, datasource_uid: str):
        """
        Makes a call to the health endpoint of a data source identified by the
        given ``uid``.

        Available in Grafana 9+.

        https://grafana.com/docs/grafana/latest/developers/http_api/data_source/#check-data-source-health
        """
        path = f"/datasources/uid/{datasource_uid}/health"
        r = self.client.GET(path)
        return r

    def find_datasource(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        get_datasource_path = "/datasources/name/%s" % datasource_name
        r = self.client.GET(get_datasource_path)
        return r

    def get_datasource_by_id(self, datasource_id):
        """
        Warning: This API is deprecated since Grafana v9.0.0 and will be
                 removed in a future release.

        :param datasource_id:
        :return:
        """
        get_datasource_path = "/datasources/%s" % datasource_id
        r = self.client.GET(get_datasource_path)
        return r

    def get_datasource_by_name(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        get_datasource_path = "/datasources/name/%s" % datasource_name
        r = self.client.GET(get_datasource_path)
        return r

    def get_datasource_by_uid(self, datasource_uid):
        """

        :param datasource_uid:
        :return:
        """
        get_datasource_path = "/datasources/uid/%s" % datasource_uid
        r = self.client.GET(get_datasource_path)
        return r

    def get_datasource_id_by_name(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        get_datasource_path = "/datasources/id/%s" % datasource_name
        r = self.client.GET(get_datasource_path)
        return r

    def get(self, dsident: DatasourceIdentifier):
        """
        Get dashboard by either datasource_id, datasource_uid, or datasource_name.
        """
        if dsident.id:
            datasource = self.get_datasource_by_id(dsident.id)
        elif dsident.uid:
            datasource = self.get_datasource_by_uid(dsident.uid)
        elif dsident.name:
            datasource = self.get_datasource_by_name(dsident.name)
        else:
            raise KeyError("Data source must be identified by one of id, uid, or name")
        return datasource

    def create_datasource(self, datasource):
        """

        :param datasource:
        :return:
        """
        create_datasources_path = "/datasources"
        r = self.client.POST(create_datasources_path, json=datasource)
        return r

    def update_datasource(self, datasource_id, datasource):
        """

        :param datasource_id:
        :param datasource:
        :return:
        """
        update_datasource = "/datasources/%s" % datasource_id
        r = self.client.PUT(update_datasource, json=datasource)
        return r

    def update_datasource_by_uid(self, datasource_uid, datasource):
        """

        :param datasource_uid:
        :param datasource:
        :return:
        """
        update_datasource = "/datasources/uid/%s" % datasource_uid
        r = self.client.PUT(update_datasource, json=datasource)
        return r

    def list_datasources(self):
        """

        :return:
        """
        list_datasources_path = "/datasources"
        r = self.client.GET(list_datasources_path)
        return r

    def delete_datasource_by_id(self, datasource_id):
        """
        Warning: This API is deprecated since Grafana v9.0.0 and will be
                 removed in a future release.

        :param datasource_id:
        :return:
        """
        delete_datasource = "/datasources/%s" % datasource_id
        r = self.client.DELETE(delete_datasource)
        return r

    def delete_datasource_by_name(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        delete_datasource = "/datasources/name/%s" % datasource_name
        r = self.client.DELETE(delete_datasource)
        return r

    def delete_datasource_by_uid(self, datasource_uid):
        """

        :param datasource_uid:
        :return:
        """
        delete_datasource = "/datasources/uid/%s" % datasource_uid
        r = self.client.DELETE(delete_datasource)
        return r

    def enable_datasource_permissions(self, datasource_id):
        """
        The Data Source Permissions is only available in Grafana Enterprise.

        :param datasource_id:
        :return:
        """
        get_datasource_path = "/datasources/%s/enable-permissions" % datasource_id
        r = self.client.POST(get_datasource_path)
        return r

    def disable_datasource_permissions(self, datasource_id):
        """
        The Data Source Permissions is only available in Grafana Enterprise.

        :param datasource_id:
        :return:
        """
        get_datasource_path = "/datasources/%s/disable-permissions" % datasource_id
        r = self.client.POST(get_datasource_path)
        return r

    def get_datasource_permissions(self, datasource_id):
        """
        The Data Source Permissions is only available in Grafana Enterprise.

        :param datasource_id:
        :return:
        """
        get_datasource_path = "/datasources/%s/permissions" % datasource_id
        r = self.client.GET(get_datasource_path)
        return r

    def add_datasource_permissions(self, datasource_id, permissions):
        """
        The Data Source Permissions is only available in Grafana Enterprise.

        :param datasource_id:
        :param permissions:
        :return:
        """
        get_datasource_path = "/datasources/%s/permissions" % datasource_id
        r = self.client.POST(get_datasource_path, json=permissions)
        return r

    def remove_datasource_permissions(self, datasource_id, permission_id):
        """
        The Data Source Permissions is only available in Grafana Enterprise.

        :param datasource_id:
        :param permission_id:
        :return:
        """
        get_datasource_path = "/datasources/%s/permissions/%s" % (datasource_id, permission_id)
        r = self.client.DELETE(get_datasource_path)
        return r

    def get_datasource_proxy_data(
        self, datasource_id, query_type="query", version="v1", expr=None, time=None, start=None, end=None, step=None
    ):
        """

        :param datasource_id:
        :param version: api_version currently v1
        :param query_type: query_range |query
        :param expr: expr to query

        :return: r (dict)
        """
        warnings.warn(
            DeprecationWarning(
                "The function `get_datasource_proxy_data()` will be removed in a future release. "
                "Please use the functions `query()`, `query_range()`, or `series()` instead."
            )
        )
        if query_type == "query":
            return self.query(datasource_id=datasource_id, query=expr, timestamp=time)
        elif query_type == "query_range":
            return self.query_range(datasource_id=datasource_id, query=expr, start=start, end=end, step=step)
        else:
            raise KeyError(f"Unknown or invalid query type: {query_type}")

    def query(self, datasource_id, query, timestamp, access="proxy"):
        """

        :param datasource_id:
        :param query:
        :param timestamp:
        :param access:
        :return:
        """
        post_query_path = "/datasources/%s/%s/api/v1/query" % (access, datasource_id)
        r = self.client.POST(
            post_query_path,
            data={
                "query": query,
                "time": timestamp,
            },
        )
        return r

    def query_range(self, datasource_id, query, start, end, step, access="proxy"):
        """

        :param datasource_id:
        :param query:
        :param start:
        :param end:
        :param step:
        :param access:
        :return:
        """
        post_query_range_path = "/datasources/%s/%s/api/v1/query_range" % (access, datasource_id)
        r = self.client.POST(post_query_range_path, data={"query": query, "start": start, "end": end, "step": step})
        return r

    def series(self, datasource_id, match, start, end, access="proxy"):
        """

        :param datasource_id:
        :param match:
        :param start:
        :param end:
        :param access:
        :return:
        """
        post_series_path = "/datasources/%s/%s/api/v1/series" % (access, datasource_id)
        r = self.client.POST(post_series_path, data={"match[]": match, "start": start, "end": end})
        return r

    def smartquery(self, datasource: Union[DatasourceIdentifier, Dict], expression: str, store: Optional[str] = None):
        """
        Send a query to the designated data source and return its response.

        TODO: This is by far not complete. The `query_factory` function has to
              be made more elaborate in order to query different data source
              types.
        """

        if isinstance(datasource, DatasourceIdentifier):
            datasource = self.get(datasource)

        datasource_id = datasource["id"]
        datasource_type = datasource["type"]
        datasource_dialect = datasource.get("jsonData", {}).get("version", "InfluxQL")
        access_type = datasource["access"]

        # Sanity checks.
        if not expression:
            raise ValueError("Expression must be given")

        # Build the query payload. Each data source has different query attributes.
        query = query_factory(datasource, expression, store)

        logger.info(f"Submitting query: {query}")

        # Compute request method, body, and endpoint.
        send_request = self.client.POST

        # Certain data sources like InfluxDB 1.x, still use the `/datasources/proxy` route.
        if datasource_type == "influxdb" and datasource_dialect == "InfluxQL":
            url = f"/datasources/proxy/{datasource_id}/query"
            if store is not None:
                url += f"?db={store}"
            payload = {"q": query["q"]}
            request_kwargs = {"data": payload}

        elif datasource_type == "graphite":
            url = f"/datasources/proxy/{datasource_id}/render"
            request_kwargs = {"data": query}

        # This case is very special. It is used for Elasticsearch and Testdata.
        elif expression.startswith("url://"):
            url = expression.replace("url://", "")
            url = url.format(
                datasource_id=datasource.get("id"),
                datasource_uid=datasource.get("uid"),
                database_name=datasource.get("database"),
            )
            request_kwargs = {}
            send_request = self.client.GET

        # For all others, use the generic data source communication endpoint.
        elif access_type in ["server", "proxy"]:
            url = "/ds/query"
            payload = {"queries": [query]}
            request_kwargs = {"json": payload}

        else:
            raise NotImplementedError(f"Unable to submit query to data source with access type '{access_type}'")

        # Submit query.
        try:
            r = send_request(url, **request_kwargs)
            # logger.debug(f"Response from generic data source query: {r}")
            return r
        except (GrafanaClientError, GrafanaServerError) as ex:
            logger.error(
                f"Querying data source failed. id={datasource_id}, type={datasource_type}. "
                f"Reason: {ex}. Response: {ex.response or '<empty>'}"
            )
            raise

    def health_check(self, datasource: Union[DatasourceIdentifier, Dict]) -> DatasourceHealthResponse:
        """
        Run a data source health check and return its success state, duration,
        and an (error) message.

        See `examples/datasource-health-check.py` for an example implementation.
        """

        if isinstance(datasource, DatasourceIdentifier):
            datasource = self.get(datasource)

        datasource_uid = datasource["uid"]
        datasource_type = datasource["type"]
        datasource_dialect = datasource.get("jsonData", {}).get("version")
        access_type = datasource["access"]

        # Sanity checks.
        if access_type not in ["server", "proxy"]:
            raise NotImplementedError(f"Unable to inquire data source with access type '{access_type}'")

        # Resolve status query by database type.
        expression = get_healthcheck_expression(datasource_type, datasource_dialect)

        start = time.time()
        try:
            response = self.smartquery(datasource, expression)
            response_display = response
            if VERBOSE:  # pragma:nocover
                response_display = json.dumps(response, indent=2)
            logger.debug(f"Health check query response is: {response_display}")
            success = False

            # Elasticsearch has a special response format.
            if datasource_type == "elasticsearch":
                database_name = datasource["database"]
                if database_name in response:
                    try:
                        _ = response[database_name]["mappings"]["properties"]
                        message = "Success"
                        success = True
                    except KeyError as ex:
                        reason = f"{ex.__class__.__name__}: {ex}"
                        message = f"Invalid response. {reason}"
                else:
                    message = f"No response for database '{database_name}'"

            # When probed, those data sources only return their own representations?
            elif datasource_type in ["fetzerch-sunandmoon-datasource", "testdata"]:
                try:
                    _ = response["id"]
                    _ = response["uid"]
                    if datasource_type == "fetzerch-sunandmoon-datasource":
                        _ = response["jsonData"]["latitude"]
                        _ = response["jsonData"]["longitude"]
                    message = "Success"
                    success = True
                except KeyError as ex:
                    reason = f"{ex.__class__.__name__}: {ex}"
                    message = f"Invalid response. {reason}"

            # Graphite has a special response format.
            elif datasource_type == "graphite":
                try:
                    result = response[0]
                    _ = result["target"]
                    _ = result["datapoints"]
                    message = "Success"
                    success = True
                except (IndexError, KeyError) as ex:
                    reason = f"{ex.__class__.__name__}: {ex}"
                    message = f"Invalid response. {reason}"

            elif datasource_type == "loki":
                if "status" in response and response["status"] == "success":
                    message = "Success"
                    success = True
                else:
                    message = response["message"]

            # With OpenTSDB, a 200 OK response with empty body is just fine.
            elif datasource_type == "opentsdb":
                message = "Success"
                success = True

            # With Tempo, a 200 OK response with a non-empty body is probably just fine.
            elif datasource_type == "tempo":
                if len(response) >= 0:
                    message = "Success"
                    success = True

            # With Zipkin, a 200 OK response with a JSON body containing an empty array is probably just fine.
            elif datasource_type == "zipkin":
                if response == []:
                    message = "Success"
                    success = True

            # Generic case, where the response has a top-level `results` or `data` key.
            else:
                if "results" in response:
                    success, message = self.parse_health_response_results(response=response)
                elif "data" in response:
                    success, message = self.parse_health_response_data(response=response)
                else:
                    message = "Response lacks expected keys 'results' or 'data'"

        except (GrafanaBadInputError, GrafanaServerError, GrafanaClientError) as ex:
            success = False
            response = ex.response
            if isinstance(response, dict):
                if datasource_type == "elasticsearch":
                    error = response["error"]
                    status_code = response["status"]
                    if "root_cause" in error:
                        error = error["root_cause"][0]
                        error_type = error["type"]
                        error_reason = error["reason"]
                        message = f"Status: {status_code}. Type: {error_type}. Reason: {error_reason}"
                    else:
                        message = str(error)

                elif "results" in ex.response:
                    message = response["results"]["test"]["error"]
                else:
                    message = f"Unknown: {ex}. Response: {response}"
            else:
                message = str(ex)

        except ReadTimeout as ex:  # pragma:nocover
            message = str(ex)
            success = False
            response = None

        duration = round(time.time() - start, 4)
        if success:
            status = "OK"
        else:
            status = "ERROR"
            logger.warning(message)

        return DatasourceHealthResponse(
            uid=datasource_uid,
            type=datasource_type,
            success=success,
            status=status,
            message=message,
            duration=duration,
            response=response,
        )

    def health_inquiry(self, datasource_uid: str) -> DatasourceHealthResponse:
        """
        Inquiry data source health. Try native method available since Grafana 9 first,
        and fall back to client-side implementation afterwards.
        """

        # Check if data source actually exists.
        try:
            datasource = self.get(DatasourceIdentifier(uid=datasource_uid))
            datasource_type = datasource["type"]
            logger.debug(f"Data source information: {datasource}")
        except GrafanaClientError as ex:
            logger.error(f"Data source with UID '{datasource_uid}' does not exist: {ex}. Response: {ex.response}")
            if ex.status_code == 404:
                message = ex.response.get("message")
                health = DatasourceHealthResponse(
                    uid=datasource_uid,
                    type=None,
                    success=False,
                    status="ERROR",
                    message=message,
                    duration=None,
                    response=ex.response,
                )
                return health
            else:
                raise

        # Check data source health.
        health = None

        # Use native Grafana 9+ data source health check.
        start = time.time()
        raised = True
        noop = False
        if self.api.version and LooseVersion(self.api.version) >= VERSION_9:
            try:
                health_native = self.health(datasource_uid=datasource_uid)
                logger.debug(f"Response from native data source health check: {health_native}")
                status = health_native["status"]
                message = health_native["message"]
                success = status == "OK"
                response = health_native
                raised = False
            except (GrafanaClientError, GrafanaServerError, GrafanaBadInputError) as ex:
                logger.warning(
                    f"Native data source health check failed. uid={datasource_uid}, ex={ex}. "
                    f"Status: {ex.status_code}. Response: {ex.response}"
                )
                message = None
                if ex.status_code in [400]:
                    status = ex.response["status"]
                    message = ex.response["message"]
                    success = False
                    response = ex.response
                    raised = False

                # When Grafana 9+ server-side health checks are not implemented yet, Grafana mostly croaks with either
                # `404 Not Found`, `Server Error 503: Plugin unavailable`, or `Server Error 504: There was an issue
                # communicating with your instance`. Let's make this a noop in order to fall back to the client-side
                # implementation.
                elif ex.status_code in [404, 503]:  # 504
                    noop = True
                elif ex.status_code >= 500:
                    status = "FATAL"
                    message = f"{ex.__class__.__name__}: {ex}"
                    success = False
                    response = ex.response
                    raised = False

                else:
                    raise

                if "code" in ex.response:
                    message = f"[{ex.response['code']}] {message}"

            finally:
                if not noop:
                    if raised:
                        raise
                    else:
                        duration = round(time.time() - start, 4)
                        health = DatasourceHealthResponse(
                            uid=datasource_uid,
                            type=datasource_type,
                            success=success,
                            status=status,
                            message=message,
                            duration=duration,
                            response=response,
                        )

        if health is None:
            # Resolve data source by UID.
            datasource = self.get(DatasourceIdentifier(uid=datasource_uid))
            # Run client-side health check.
            health = self.health_check(datasource=datasource)

        return health

    @staticmethod
    def parse_health_response_results(response: Dict) -> Tuple[bool, str]:
        success = False
        results = response["results"]
        if isinstance(results, dict):
            try:

                # The `refId` currently used is always `test`, see `knowledge.py`.
                # TODO: Change to `gcX`.
                result = results["test"]

                # Handle response in new DataFrame format.
                # Data frames are available in Grafana 7.0+, and replaced the Time series and Table structures
                # with a more generic data structure that can support a wider range of data types.
                # -- https://grafana.com/docs/grafana/latest/developers/plugins/data-frames/
                if "frames" in result:
                    if not isinstance(result["frames"], list):
                        raise TypeError("DataFrame response detected, but 'frames' is not a list")
                    try:
                        message = result["frames"][0]["schema"]["meta"]["executedQueryString"]
                    except (IndexError, KeyError):
                        message = "Success"
                    success = True

                # Handle response in previous format, where the `refId` is reflected on the top-level.
                elif "refId" in result:
                    try:
                        message = result["meta"]["executedQueryString"]
                    except KeyError:
                        message = "Success"
                    success = True
                else:
                    raise TypeError("Invalid response format")
            except TypeError as ex:
                reason = f"{ex.__class__.__name__}: {ex}"
                message = f"FATAL: Unable to decode result from dictionary-type response. {reason}"

        # Evaluate first item when `results` is a list.
        elif isinstance(results, list):
            try:
                result = results[0]
                if "error" in result:
                    message = result["error"]
                else:
                    _ = result["statement_id"]
                    _ = result["series"]
                    message = "Success"
                    success = True
            except (IndexError, KeyError) as ex:
                reason = f"{ex.__class__.__name__}: {ex}"
                message = f"FATAL: Unable to decode result from list-type response. {reason}"
        else:
            message = f"FATAL: Unknown response type '{type(results)}'. Expected: dictionary or list."

        return success, message

    @staticmethod
    def parse_health_response_data(response: Dict) -> Tuple[bool, str]:
        """
        Response from Jaeger::

            {"data":["jaeger-query"],"total":1,"limit":0,"offset":0,"errors":null}

        Response from Loki::

            {"status":"success","data":["__name__"]}

        """
        success = False
        message = str(response["data"])
        if "errors" in response and response["errors"]:
            message = str(response["errors"])
        else:
            success = True

        return success, message
