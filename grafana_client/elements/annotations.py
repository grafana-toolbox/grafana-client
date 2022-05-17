from .base import Base


class Annotations(Base):
    def __init__(self, client):
        super(Annotations, self).__init__(client)
        self.client = client

    def get_annotation(
        self,
        time_from=None,
        time_to=None,
        alert_id=None,
        dashboard_id=None,
        panel_id=None,
        user_id=None,
        ann_type=None,
        tags=None,
        limit=None,
    ):

        """
        https://grafana.com/docs/grafana/latest/http_api/annotations/#find-annotations

        :param time_from:
        :param time_to:
        :param alert_id:
        :param dashboard_id:
        :param panel_id:
        :param user_id:
        :param ann_type: Annotation type. On of alert|annotation
        :param tags:
        :param limit:
        :return:
        """
        list_annotations_path = "/annotations"
        params = []

        if time_from:
            params.append("from=%s" % time_from)

        if time_to:
            params.append("to=%s" % time_to)

        if alert_id:
            params.append("alertId=%s" % alert_id)

        if dashboard_id:
            params.append("dashboardId=%s" % dashboard_id)

        if panel_id:
            params.append("panelId=%s" % panel_id)

        if user_id:
            params.append("userId=%s" % user_id)

        if ann_type:
            params.append("type=%s" % ann_type)

        if tags:
            for tag in tags:
                params.append("tags=%s" % tag)

        if limit:
            params.append("limit=%s" % limit)

        list_annotations_path += "?"
        list_annotations_path += "&".join(params)

        r = self.client.GET(list_annotations_path)

        return r

    def add_annotation(
        self,
        dashboard_id=None,
        panel_id=None,
        time_from=None,
        time_to=None,
        tags=[],
        text=None,
    ):

        """
        https://grafana.com/docs/grafana/latest/http_api/annotations/#create-annotation

        :param dashboard_id:
        :param panel_id
        :param time_from:
        :param time_to:
        :param tags:
        :param text:
        :return:
        """

        annotations_path = "/annotations"
        payload = {
            "dashboardId": dashboard_id,
            "panelId": panel_id,
            "time": time_from,
            "timeEnd": time_to,
            "tags": tags,
            "text": text,
        }

        r = self.client.POST(annotations_path, json=payload)

        return r

    def add_annotation_graphite(
        self,
        what=None,
        tags=[],
        when=None,
        data=None,
    ):
        """
        https://grafana.com/docs/grafana/latest/http_api/annotations/#create-annotation-in-graphite-format

        :param what:
        :param tags:
        :param when:
        :param data:
        :return:
        """

        annotations_path = "/annotations/graphite"
        payload = {"what": what, "tags": tags, "when": when, "data": data}

        r = self.client.POST(annotations_path, json=payload)

        return r

    def update_annotation(
        self,
        annotations_id,
        time_from=None,
        time_to=None,
        tags=[],
        text=None,
    ):
        """
        https://grafana.com/docs/grafana/latest/http_api/annotations/#update-annotation

        :param time_from:
        :param time_to:
        :param tags:
        :param text:
        :return:
        """
        annotations_path = "/annotations/{}".format(annotations_id)
        payload = {"time": time_from, "timeEnd": time_to, "tags": tags, "text": text}

        r = self.client.PUT(annotations_path, json=payload)

        return r

    def partial_update_annotation(
        self,
        annotations_id,
        time_from=None,
        time_to=None,
        tags=[],
        text=None,
    ):
        """
        https://grafana.com/docs/grafana/latest/http_api/annotations/#patch-annotation

        :param annotations_id:
        :param time_from:
        :param time_to:
        :param tags:
        :param text:
        :return:
        """
        annotations_path = "/annotations/{}".format(annotations_id)
        payload = {}

        payload = {"time": time_from, "timeEnd": time_to, "tags": tags, "text": text}

        r = self.client.PATCH(annotations_path, json=payload)

        return r

    def delete_annotations_by_id(self, annotations_id=None):

        """
        https://grafana.com/docs/grafana/latest/http_api/annotations/#delete-annotation-by-id

        :param annotations_id:
        :return:
        """
        annotations_path = "/annotations/{}".format(annotations_id)
        r = self.client.DELETE(annotations_path)

        return r
