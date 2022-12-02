from ..model import PersonalPreferences
from .base import Base


class Users(Base):
    def __init__(self, client):
        super(Users, self).__init__(client)
        self.client = client

    def search_users(self, query=None, page=None, perpage=None):
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
                users_on_page = self.client.GET(url)
                if not users_on_page:
                    break
                list_of_users += users_on_page
                page += 1
        else:
            users_on_page = self.client.GET(show_users_path)
            list_of_users += users_on_page

        return list_of_users

    def get_user(self, user_id):
        """

        :param user_id:
        :return:
        """
        get_user_path = "/users/%s" % user_id
        r = self.client.GET(get_user_path)
        return r

    def find_user(self, login_or_email):
        """

        :param login_or_email:
        :return:
        """
        search_user_path = "/users/lookup?loginOrEmail=%s" % login_or_email
        r = self.client.GET(search_user_path)
        return r

    def update_user(self, user_id, user):
        """

        :param user_id:
        :param user:
        :return:
        """
        update_user_path = "/users/%s" % user_id
        r = self.client.PUT(update_user_path, json=user)
        return r

    def get_user_organisations(self, user_id):
        """

        :param user_id:
        :return:
        """
        get_user_organisations_path = "/users/%s/orgs" % user_id
        r = self.client.GET(get_user_organisations_path)
        return r


class User(Base):
    def __init__(self, client):
        super(User, self).__init__(client)
        self.client = client
        self.path = "/user"

    def get_actual_user(self):
        """

        :return:
        """
        get_actual_user_path = "/user"
        r = self.client.GET(get_actual_user_path)
        return r

    def change_actual_user_password(self, old_password, new_password):
        """

        :param old_password:
        :param new_password:
        :return:
        """
        change_actual_user_password_path = "/user/password"
        change_actual_user_password_json = {
            "oldPassword": old_password,
            "newPassword": new_password,
            "confirmNew": new_password,
        }
        r = self.client.PUT(change_actual_user_password_path, json=change_actual_user_password_json)
        return r

    def switch_user_organisation(self, user_id, organisation_id):
        """

        :param user_id:
        :param organisation_id:
        :return:
        """
        switch_user_organisation_path = "/users/%s/using/%s" % (
            user_id,
            organisation_id,
        )
        r = self.client.POST(switch_user_organisation_path)
        return r

    def switch_actual_user_organisation(self, organisation_id):
        """

        :param organisation_id:
        :return:
        """
        switch_actual_user_organisation_path = "/user/using/%s" % organisation_id
        r = self.client.POST(switch_actual_user_organisation_path)
        return r

    def get_actual_user_organisations(self):
        """

        :return:
        """
        get_actual_user_organisations_path = "/user/orgs"
        r = self.client.GET(get_actual_user_organisations_path)
        return r

    def star_actual_user_dashboard(self, dashboard_id):
        """

        :param dashboard_id:
        :return:
        """
        star_dashboard = "/user/stars/dashboard/%s" % dashboard_id
        r = self.client.POST(star_dashboard)
        return r

    def unstar_actual_user_dashboard(self, dashboard_id):
        """

        :param dashboard_id:
        :return:
        """
        unstar_dashboard = "/user/stars/dashboard/%s" % dashboard_id
        r = self.client.DELETE(unstar_dashboard)
        return r

    def get_preferences(self):
        """
        Retrieve preferences of current user.

        :return:
        """
        update_preference = "/user/preferences"
        r = self.client.GET(update_preference)
        return r

    def update_preferences(self, preferences: PersonalPreferences):
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

        r = self.client.PUT(
            update_preference,
            json=data,
        )
        return r

    def patch_preferences(self, preferences: PersonalPreferences):
        """
        Update specific preferences of current user.

        From the `preferences` instance, only attributes with values `not None` will be submitted
        and updated.

        :param preferences:
        :return:
        """
        update_preference = "/user/preferences"
        data = preferences.asdict(filter_none=True)

        r = self.client.PATCH(
            update_preference,
            json=data,
        )
        return r
