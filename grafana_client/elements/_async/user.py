from ...model import PersonalPreferences
from ..base import Base


class Users(Base):
    def __init__(self, client):
        super(Users, self).__init__(client)
        self.client = client

    async def search_users(self, query=None, page=None, perpage=None):
        """

        :return:
        """
        list_of_users = []
        users_on_page = None
        show_users_path = "/users"
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

        show_users_path += "?"
        show_users_path += "&".join(params)

        if iterate:
            while True:
                url = show_users_path % page
                users_on_page = await self.client.GET(url)
                if not users_on_page:
                    break
                list_of_users += users_on_page
                page += 1
        else:
            users_on_page = await self.client.GET(show_users_path)
            list_of_users += users_on_page

        return list_of_users

    async def get_user(self, user_id):
        """

        :param user_id:
        :return:
        """
        get_user_path = "/users/%s" % user_id
        return await self.client.GET(get_user_path)

    async def find_user(self, login_or_email):
        """

        :param login_or_email:
        :return:
        """
        search_user_path = "/users/lookup?loginOrEmail=%s" % login_or_email
        return await self.client.GET(search_user_path)

    async def update_user(self, user_id, user):
        """

        :param user_id:
        :param user:
        :return:
        """
        update_user_path = "/users/%s" % user_id
        return await self.client.PUT(update_user_path, json=user)

    async def get_user_organisations(self, user_id):
        """

        :param user_id:
        :return:
        """
        get_user_organisations_path = "/users/%s/orgs" % user_id
        return await self.client.GET(get_user_organisations_path)

    async def get_user_teams(self, user_id):
        """

        :param user_id:
        :return:
        """
        get_user_teams_path = "/users/%s/teams" % user_id
        return await self.client.GET(get_user_teams_path)


class User(Base):
    def __init__(self, client):
        super(User, self).__init__(client)
        self.client = client
        self.path = "/user"

    async def get_actual_user(self):
        """

        :return:
        """
        get_actual_user_path = "/user"
        return await self.client.GET(get_actual_user_path)

    async def change_actual_user_password(self, old_password, new_password):
        """

        :param old_password:
        :param new_password:
        :return:
        """
        change_actual_user_password_path = "/user/password"  # noqa: S105
        change_actual_user_password_json = {
            "oldPassword": old_password,
            "newPassword": new_password,
            "confirmNew": new_password,
        }
        return await self.client.PUT(change_actual_user_password_path, json=change_actual_user_password_json)

    async def switch_user_organisation(self, user_id, organisation_id):
        """

        :param user_id:
        :param organisation_id:
        :return:
        """
        switch_user_organisation_path = "/users/%s/using/%s" % (
            user_id,
            organisation_id,
        )
        return await self.client.POST(switch_user_organisation_path)

    async def switch_actual_user_organisation(self, organisation_id):
        """

        :param organisation_id:
        :return:
        """
        switch_actual_user_organisation_path = "/user/using/%s" % organisation_id
        return await self.client.POST(switch_actual_user_organisation_path)

    async def get_actual_user_organisations(self):
        """

        :return:
        """
        get_actual_user_organisations_path = "/user/orgs"
        return await self.client.GET(get_actual_user_organisations_path)

    async def get_actual_user_teams(self):
        """

        :return:
        """
        get_actual_user_teams_path = "/user/teams"
        return await self.client.GET(get_actual_user_teams_path)

    async def star_actual_user_dashboard(self, dashboard_id):
        """

        :param dashboard_id:
        :return:
        """
        star_dashboard = "/user/stars/dashboard/%s" % dashboard_id
        return await self.client.POST(star_dashboard)

    async def unstar_actual_user_dashboard(self, dashboard_id):
        """

        :param dashboard_id:
        :return:
        """
        unstar_dashboard = "/user/stars/dashboard/%s" % dashboard_id
        return await self.client.DELETE(unstar_dashboard)

    async def get_preferences(self):
        """
        Retrieve preferences of current user.

        :return:
        """
        update_preference = "/user/preferences"
        return await self.client.GET(update_preference)

    async def update_preferences(self, preferences: PersonalPreferences):
        """
        Update preferences of current user as a whole.

        From the `preferences` instance, only attributes with values `not None` will be submitted.
        However, Grafana will reset all undefined attributes to its internal defaults.

        If you want to update specific preference attributes, without touching the others,
        please use the `patch_preferences` method.

        :param preferences:
        :return:
        """
        update_preference = "/user/preferences"
        data = preferences.asdict(filter_none=True)

        return await self.client.PUT(
            update_preference,
            json=data,
        )

    async def patch_preferences(self, preferences: PersonalPreferences):
        """
        Update specific preferences of current user.

        From the `preferences` instance, only attributes with values `not None` will be submitted
        and updated.

        :param preferences:
        :return:
        """
        update_preference = "/user/preferences"
        data = preferences.asdict(filter_none=True)

        return await self.client.PATCH(
            update_preference,
            json=data,
        )
