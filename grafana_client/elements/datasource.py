import json
import logging
import time
from typing import Dict

from ..client import GrafanaBadInputError, GrafanaClientError, GrafanaServerError
from ..knowledge import get_healthcheck_expression, query_factory
from ..model import DatasourceHealth
from .base import Base

logger = logging.getLogger(__name__)

VERBOSE = False


class Datasource(Base):
    def __init__(self, client):
        super(Datasource, self).__init__(client)
        self.client = client

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

    def get(self, datasource_id: str = None, datasource_uid: str = None, datasource_name: str = None):
        """
        Get dashboard by either datasource_id, datasource_uid, or datasource_name.
        """
        if datasource_id:
            datasource = self.get_datasource_by_id(datasource_id)
        elif datasource_uid:
            datasource = self.get_datasource_by_uid(datasource_uid)
        elif datasource_name:
            datasource = self.get_datasource_by_name(datasource_name)
        else:
            raise KeyError("Either datasource_id or datasource_name must be given")
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
        get_datasource_path = "/datasources/proxy/{0}" "/api/{1}/{2}?query={3}".format(
            datasource_id, version, query_type, expr
        )
        if query_type == "query_range":
            get_datasource_path = get_datasource_path + "&start={0}&end={1}&step={2}".format(start, end, step)
        else:
            get_datasource_path = get_datasource_path + "&time={}".format(time)
        r = self.client.GET(get_datasource_path)
        return r

    def query(self, datasource: Dict, expression: str):
        """
        Send a query to the designated data source and return its response.
        """

        datasource_id = datasource["id"]
        datasource_type = datasource["type"]
        datasource_dialect = datasource.get("jsonData", {}).get("version")
        access_type = datasource["access"]

        # Sanity checks.
        if not expression:
            raise ValueError("Expression must be given")

        # Build the query payload. Each data source has different query attributes.
        query = query_factory(datasource, expression)

        # Compute request method, body, and endpoint.
        send_request = self.client.POST

        # Certain data sources like InfluxDB 1.x, still use the `/datasources/proxy` route.
        if datasource_type == "influxdb" and datasource_dialect == "InfluxQL":
            url = f"/datasources/proxy/{datasource_id}/query"
            payload = {"q": query["q"]}
            request_kwargs = {"data": payload}

        # This case is very special. It is used for Elasticsearch and Testdata.
        elif expression.startswith("url://"):
            url = expression.replace("url://", "")
            url = url.format(
                datasource_id=datasource["id"], datasource_uid=datasource["uid"], database_name=datasource["database"]
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
            return r
        except (GrafanaServerError, GrafanaClientError) as ex:
            logger.error(
                f"Unable to query data source id={datasource_id}, type={datasource_type}. Reason: {ex}. Response: {ex.response}"
            )
            raise

    def health_check(self, datasource: Dict):
        """
        Run a data source health check and return its success state, duration,
        and an (error) message.

        See `examples/datasource.py` for an example implementation.
        """

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
            response = self.query(datasource, expression)
            response_display = response
            if VERBOSE:
                response_display = json.dumps(response, indent=2)
            logger.debug(f"Health check query response is: {response_display}")
            success = False

            # This case is very special. It is used for Elasticsearch and Testdata.
            if datasource_type == "elasticsearch":
                database_name = datasource["database"]
                assert response[database_name]["mappings"]["properties"], "Invalid response from Elasticsearch"
                message = "Success"
                success = True
            elif datasource_type == "testdata":
                assert response["id"], "Invalid response from Testdata. No attribute 'id' in response."
                assert response["uid"], "Invalid response from Testdata. No attribute 'uid' in response."
                message = "Success"
                success = True

            # Generic case, where the response has a top-level "results" key.
            else:
                results = response["results"]

                # Evaluate response when the "refId" is reflected.
                if isinstance(results, dict):
                    try:
                        result = results["test"]
                        # Grafana 9 and up uses the DataFrame format.
                        if "frames" in result:
                            message = result["frames"][0]["schema"]["meta"]["executedQueryString"]
                            success = True
                        # Grafana 7 and 8 use the previous format.
                        elif "refId" in result:
                            # Grafana 8
                            try:
                                message = result["meta"]["executedQueryString"]
                            # Grafana 7
                            except KeyError:
                                message = "Success"
                            success = True
                        else:
                            raise KeyError(f"Unexpected result format")
                    except (KeyError, IndexError, AssertionError) as ex:
                        message = f"FATAL: Unable to decode result from dictionary-type response: {ex}"
                        logger.warning(message)

                # Evaluate first item when `results` is a list.
                elif isinstance(results, list):
                    try:
                        result = results[0]
                        if "error" in result:
                            message = result["error"]
                        else:
                            assert "statement_id" in result, "No 'statement_id' in result"
                            assert "series" in result, "No 'series' in result"
                            message = "Success"
                            success = True
                    except (KeyError, IndexError, AssertionError) as ex:
                        message = f"FATAL: Unable to decode result from list-type response: {ex}"
                        logger.warning(message)
                else:
                    raise KeyError(f"Unknown response type for data source type {datasource_type}: {type(results)}")

        except (GrafanaBadInputError, GrafanaServerError, GrafanaClientError) as ex:
            success = False
            response = ex.response
            if isinstance(ex.response, dict):
                if datasource_type == "elasticsearch":
                    error = ex.response["error"]
                    status_code = ex.response["status"]
                    if "root_cause" in error:
                        error = error["root_cause"][0]
                        error_type = error["type"]
                        error_reason = error["reason"]
                        message = f"Status: {status_code}. Type: {error_type}. Reason: {error_reason}"
                    else:
                        message = str(error)

                elif "results" in ex.response:
                    message = ex.response["results"]["test"]["error"]
                else:
                    message = f"Unknown: {ex}. Response: {ex.response}"
            else:
                message = str(ex)

        duration = round(time.time() - start, 4)
        return DatasourceHealth(success=success, message=message, duration=duration, response=response)
