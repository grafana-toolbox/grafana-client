from .base import Base


class Organization(Base):
    def __init__(self, api):
        super(Organization, self).__init__(api)
        self.api = api

    def find_organization(self, org_name):
        """

        :param org_name:
        :return:
        """
        get_org_path = "/orgs/name/%s" % org_name
        r = self.api.GET(get_org_path)
        return r

    def get_current_organization(self):
        """

        :return:
        """
        get_current_organization_path = "/org"
        r = self.api.GET(get_current_organization_path)
        return r

    def create_organization(self, organization):
        """

        :param organization:
        :return:
        """
        create_orgs_path = "/orgs"
        r = self.api.POST(create_orgs_path, json={"name": organization["name"]})
        return r

    def update_current_organization(self, organization):
        """

        :param organization:
        :return:
        """
        update_current_organization_path = "/org"
        r = self.api.PUT(update_current_organization_path, json=organization)
        return r

    def get_current_organization_users(self):
        """

        :return:
        """
        get_current_organization_users_path = "/org/users"
        r = self.api.GET(get_current_organization_users_path)
        return r

    def add_user_current_organization(self, user):
        """

        :param user:
        :return:
        """
        add_user_current_organization_path = "/org/users"
        r = self.api.POST(add_user_current_organization_path, json=user)
        return r

    def update_user_current_organization(self, user_id, user):
        """

        :param user_id:
        :param user:
        :return:
        """
        update_user_current_organization_path = "/org/users/%s" % user_id
        r = self.api.PATCH(update_user_current_organization_path, json=user)
        return r

    def delete_user_current_organization(self, user_id):
        """

        :param user_id:
        :return:
        """
        delete_user_current_organization_path = "/org/users/%s" % user_id
        r = self.api.DELETE(delete_user_current_organization_path)
        return r


class Organizations(Base):
    def __init__(self, api):
        super(Organizations, self).__init__(api)
        self.api = api
        self.path = "/users"

    def update_organization(self, organization_id, organization):
        """

        :param organization_id:
        :param organization:
        :return:
        """
        update_org_path = "/orgs/%s" % organization_id
        r = self.api.PUT(update_org_path, json=organization)
        return r

    def delete_organization(self, organization_id):
        """

        :param organization_id:
        :return:
        """
        delete_org_path = "/orgs/%s" % organization_id
        r = self.api.DELETE(delete_org_path)
        return r

    def list_organization(self):
        """

        :return:
        """
        search_org_path = "/orgs"
        r = self.api.GET(search_org_path)
        return r

    def switch_organization(self, organization_id):
        """

        :param organization_id:
        :return:
        """
        switch_user_organization = "/user/using/%s" % organization_id
        r = self.api.POST(switch_user_organization)
        return r

    def organization_user_list(self, organization_id):
        """

        :param organization_id:
        :return:
        """
        users_in_org = "/orgs/%s/users" % organization_id
        r = self.api.GET(users_in_org)
        return r

    def organization_user_add(self, organization_id, user):
        """

        :param organization_id:
        :param user:
        :return:
        """
        add_user_path = "/orgs/%s/users" % organization_id
        r = self.api.POST(add_user_path, json=user)
        return r

    def organization_user_update(self, organization_id, user_id, user_role):
        """

        :param organization_id:
        :param user_id:
        :param user_role:
        :return:
        """
        patch_user = "/orgs/%s/users/%s" % (organization_id, user_id)
        r = self.api.PATCH(patch_user, json={"role": user_role})
        return r

    def organization_user_delete(self, organization_id, user_id):
        """

        :param organization_id:
        :param user_id:
        :return:
        """
        delete_user = "/orgs/%s/users/%s" % (organization_id, user_id)
        r = self.api.DELETE(delete_user)
        return r

    def organization_preference_get(self):
        """
        :return:
        """
        update_preference = "/org/preferences"
        r = self.api.GET(update_preference)
        return r

    def organization_preference_update(
        self, theme="", home_dashboard_id=0, timezone="utc"
    ):
        """

        :param theme:
        :param home_dashboard_id:
        :param timezone:
        :return:
        """
        update_preference = "/org/preferences"
        r = self.api.PUT(
            update_preference,
            json={
                "theme": theme,
                "homeDashboardId": home_dashboard_id,
                "timezone": timezone,
            },
        )
        return r
