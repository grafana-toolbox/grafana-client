from verlib2 import Version

from ..base import Base

VERSION_8_2 = Version("8.2")


class LibraryElement(Base):
    Panel: int = 1
    Variable: int = 2

    def __init__(self, client, api):
        super(LibraryElement, self).__init__(client)
        self.client = client
        self.api = api

    async def get_library_element(self, element_uid: str) -> any:
        """

        :param element_uid:
        :return:
        """
        if await self.api.version and Version(await self.api.version) < VERSION_8_2:
            raise DeprecationWarning("Grafana versions earlier than 8.2 do not support library elements")
        get_element_path = f"/library-elements/{element_uid}"
        return await self.client.GET(get_element_path)

    async def get_library_element_by_name(self, element_name: str) -> any:
        """

        :param element_name:
        :return:
        """
        if await self.api.version and Version(await self.api.version) < VERSION_8_2:
            raise DeprecationWarning("Grafana versions earlier than 8.2 do not support library elements")
        get_element_path = f"/library-elements/name/{element_name}"
        return await self.client.GET(get_element_path)

    async def get_library_element_connections(self, element_uid: str) -> any:
        """

        :param element_uid:
        :return:
        """
        if await self.api.version and Version(await self.api.version) < VERSION_8_2:
            raise DeprecationWarning("Grafana versions earlier than 8.2 do not support library elements")
        get_element_connections_path = f"/library-elements/{element_uid}/connections"
        return await self.client.GET(get_element_connections_path)

    async def create_library_element(
        self, model: dict, name: str = None, kind: int = Panel, uid: str = None, folder_uid: str = None
    ):
        """

        :param model:
        :param name:
        :param kind:
        :param uid:
        :param folder_uid:
        :return:
        """
        if await self.api.version and Version(await self.api.version) < VERSION_8_2:
            raise DeprecationWarning("Grafana versions earlier than 8.2 do not support library elements")
        json: dict = dict()
        # If the model contains a "meta" entry, use the "folderUid" entry if folder_uid isn't given
        if folder_uid is not None:
            json["folderUid"] = folder_uid
        elif "meta" in model and "folderUid" in model["meta"]:
            json["folderUid"] = model["meta"]["folderUid"]
        # If the model contains a "model" entry, use the "uid" entry if uid isn't given
        if uid is not None:
            json["uid"] = uid
        elif "model" in model and "uid" in model["model"]:
            json["uid"] = model["model"]["uid"]
        # If the model contains a "model" entry, use the "title" entry if title isn't given
        if name is not None:
            json["name"] = name
        elif "model" in model and "title" in model["model"]:
            json["name"] = model["model"]["title"]
        if "model" in model:
            json["model"] = model["model"]
        else:
            json["model"] = model
        # If the model contains a "kind" entry, use that instead of the specified kind
        if "kind" in model:
            json["kind"] = model["kind"]
        else:
            json["kind"] = kind
        create_element_path = "/library-elements"
        return await self.client.POST(create_element_path, json=json)

    async def update_library_element(
        self, uid: str, model: dict, name: str = None, kind: int = Panel, folder_uid: str = None, version: int = None
    ):
        """

        :param uid:
        :param model:
        :param name:
        :param kind:
        :param folder_uid:
        :return:
        """
        if await self.api.version and Version(await self.api.version) < VERSION_8_2:
            raise DeprecationWarning("Grafana versions earlier than 8.2 do not support library elements")
        json: dict = dict()
        # If the model contains a "meta" entry, use the "folderUid" entry if folder_uid isn't given
        if folder_uid is not None:
            json["folderUid"] = folder_uid
        elif "meta" in model and "folderUid" in model["meta"]:
            json["folderUid"] = model["meta"]["folderUid"]
        json["uid"] = uid
        # If the model contains a "model" entry, use the "title" entry if title isn't given
        if name is not None:
            json["name"] = name
        elif "model" in model and "title" in model["model"]:
            json["name"] = model["model"]["title"]
        if "model" in model:
            json["model"] = model["model"]
        else:
            json["model"] = model
        # If the model contains a "kind" entry, use that instead of the specified kind
        if "kind" in model:
            json["kind"] = model["kind"]
        else:
            json["kind"] = kind
        if version is None:
            current_element = await self.get_library_element(uid)
            if "version" in current_element:
                json["version"] = current_element["version"]
            else:
                raise ValueError("version must be specified")
        else:
            json["version"] = version

        update_element_path = f"/library-elements/{uid}"
        return await self.client.PATCH(update_element_path, json=json)

    async def delete_library_element(self, element_uid: str) -> any:
        """

        :param element_uid:
        :return:
        """
        if await self.api.version and Version(await self.api.version) < VERSION_8_2:
            raise DeprecationWarning("Grafana versions earlier than 8.2 do not support library elements")
        delete_element_path = f"/library-elements/{element_uid}"
        return await self.client.DELETE(delete_element_path)

    async def list_library_elements(
        self,
        search_string: str = None,
        kind: int = None,
        sort_direction: str = None,
        type_filter: str = None,
        exclude_uid: str = None,
        folder_filter: str = None,
        per_page: int = None,
        page: int = None,
    ) -> any:
        """

        :param search_string:
        :param kind:
        :param sort_direction:
        :param type_filter:
        :param exclude_uid:
        :param folder_filter:
        :param per_page:
        :param page:

        :return:
        """
        if await self.api.version and Version(await self.api.version) < VERSION_8_2:
            raise DeprecationWarning("Grafana versions earlier than 8.2 do not support library elements")
        list_elements_path = "/library-elements"
        params = []

        if search_string is not None:
            params.append("searchString=%s" % search_string)
        if kind is not None:
            params.append("kind=%d" % kind)
        if sort_direction is not None:
            params.append("sortDirection=%s" % sort_direction)
        if type_filter is not None:
            params.append("typeFilter=%s" % type_filter)
        if exclude_uid is not None:
            params.append("excludeUid=%s" % exclude_uid)
        if folder_filter is not None:
            params.append("folderFilter=%s" % folder_filter)
        if per_page is not None:
            params.append("perPage=%d" % per_page)
        if page is not None:
            params.append("page=%d" % page)

        list_elements_path += "?"
        list_elements_path += "&".join(params)
        return await self.client.GET(list_elements_path)
