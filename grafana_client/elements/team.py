import typing as t
import warnings

from verlib2 import Version

from ..model import PersonalPreferences
from .base import Base

VERSION_10_2_0 = Version("10.2.0")


class Teams(Base):
    def __init__(self, client, api):
        super(Teams, self).__init__(client)
        self.client = client
        self.api = api

    def search_teams(self, query=None, page=None, perpage=None):
        """

        :return:
        """
        list_of_teams = []
        search_teams_path = "/teams/search"
        params = []

        if query:
            params.append("query=%s" % query)

        if page:
            iterate = False
            params.append("page=%s" % page)
        else:
            iterate = True
            params.append("page=%s")
            page = 1

        if perpage:
            params.append("perpage=%s" % perpage)

        search_teams_path += "?"
        search_teams_path += "&".join(params)

        if iterate:
            while True:
                teams_on_page = self.client.GET(search_teams_path % page)
                list_of_teams += teams_on_page["teams"]
                if len(teams_on_page["teams"]) < teams_on_page["perPage"]:
                    break
                page += 1
        else:
            teams_on_page = self.client.GET(search_teams_path)
            list_of_teams += teams_on_page["teams"]

        return list_of_teams

    def get_team_by_name(self, team_name):
        """

        :param team_name:
        :return:
        """
        search_teams_path = "/teams/search"

        search_teams_path += "?name=%s" % team_name

        teams_on_page = self.client.GET(search_teams_path)
        return teams_on_page["teams"]

    def get_team(self, team_id):
        """

        :param team_id:
        :return:
        """
        get_team_path = "/teams/%s" % team_id
        return self.client.GET(get_team_path)

    def add_team(self, team):
        """

        :param team:
        :return:
        """
        add_team_path = "/teams"
        return self.client.POST(add_team_path, json=team)

    def update_team(self, team_id, team):
        """

        :param team_id:
        :param team:
        :return:
        """
        update_team_path = "/teams/%s" % team_id
        return self.client.PUT(update_team_path, json=team)

    def delete_team(self, team_id):
        """

        :param team_id:
        :return:
        """
        delete_team_path = "/teams/%s" % team_id
        return self.client.DELETE(delete_team_path)

    def get_team_members(self, team_id):
        """

        :param team_id:
        :return:
        """
        get_team_members_path = "/teams/%s/members" % team_id
        return self.client.GET(get_team_members_path)

    def add_team_member(self, team_id, user_id):
        """

        :param team_id:
        :param user_id:
        :return:
        """
        add_team_member_path = "/teams/%s/members" % team_id
        payload = {"userId": user_id}
        return self.client.POST(add_team_member_path, json=payload)

    def remove_team_member(self, team_id, user_id):
        """

        :param team_id:
        :param user_id:
        :return:
        """
        remove_team_member_path = "/teams/%s/members/%s" % (team_id, user_id)
        return self.client.DELETE(remove_team_member_path)

    def get_team_preferences(self, team_id: int):
        """

        :param team_id:
        :return:
        """
        warnings.warn("This method is deprecated, please use `get_preferences`", DeprecationWarning)
        return self.get_preferences(team_id=team_id)

    def update_team_preferences(self, team_id: int, preferences: t.Dict):
        """

        :param team_id:
        :param preferences:
        :return:
        """
        warnings.warn("This method is deprecated, please use `update_preferences`", DeprecationWarning)
        preferences = PersonalPreferences(**preferences)
        return self.update_preferences(team_id=team_id, preferences=preferences)

    def get_preferences(self, team_id: int):
        """

        :param team_id:
        :return:
        """
        get_team_preferences_path = "/teams/%s/preferences" % team_id
        return self.client.GET(get_team_preferences_path)

    def update_preferences(self, team_id: int, preferences: PersonalPreferences):
        """

        :param team_id:
        :param preferences:
        :return:
        """
        update_team_preferences_path = "/teams/%s/preferences" % team_id
        if isinstance(preferences, PersonalPreferences):
            data = preferences.asdict(filter_none=True)
        else:
            raise TypeError(
                f"Unable to use data type '{type(preferences)}' for updating preferences. "
                f"Please use `PersonalPreferences` instead."
            )
        return self.client.PUT(update_team_preferences_path, json=data)

    def get_team_external_group(self, team_id):
        """
        The External Group Synchronization is only available in Grafana Enterprise.

        :param team_id:
        :return:
        """
        team_group_path = "/teams/%s/groups" % team_id
        return self.client.GET(team_group_path)

    def add_team_external_group(self, team_id, group):
        """
        The External Group Synchronization is only available in Grafana Enterprise.

        :param team_id:
        :param group:
        :return:
        """
        team_group_path = "/teams/%s/groups" % team_id
        return self.client.POST(team_group_path, json={"groupId": group})

    def remove_team_external_group(self, team_id, group_id):
        """
        The External Group Synchronization is only available in Grafana Enterprise.

        :param team_id:
        :param group_id:
        :return:
        """
        if Version(self.api.version) < VERSION_10_2_0:
            team_group_path = "/teams/%s/groups/%s" % (team_id, group_id)
        else:
            team_group_path = "/teams/%s/groups?groupId=%s" % (team_id, group_id)
        return self.client.DELETE(team_group_path)
