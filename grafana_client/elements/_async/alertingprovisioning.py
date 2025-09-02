from ..base import Base


class AlertingProvisioning(Base):
    def __init__(self, client):
        super(AlertingProvisioning, self).__init__(client)
        self.client = client

    async def get_alertrules_all(self):
        """
        Gets all alert rules
        @return:
        """
        get_alertrules_all_path = "/v1/provisioning/alert-rules"
        return await self.client.GET(get_alertrules_all_path)

    async def get_alertrule(self, alertrule_uid):
        """

        :param alertrule_uid:
        :return:
        """
        get_alertrule_path = "/v1/provisioning/alert-rules/%s" % alertrule_uid
        return await self.client.GET(get_alertrule_path)

    async def create_alertrule(self, alertrule, disable_provenance=False):
        """
        :param alertrule:
        :param disable_provenance:
        :return:
        """
        create_alertrule_path = "/v1/provisioning/alert-rules"
        headers = {}
        if disable_provenance:
            headers["X-Disable-Provenance"] = "true"
        return await self.client.POST(create_alertrule_path, json=alertrule, headers=headers)

    async def update_alertrule(self, alertrule_uid, alertrule, disable_provenance=False):
        """
        :param alertrule_uid:
        :param alertrule:
        :param disable_provenance:
        :return:
        """
        update_alertrule_path = "/v1/provisioning/alert-rules/%s" % alertrule_uid
        headers = {}
        if disable_provenance:
            headers["X-Disable-Provenance"] = "true"
        return await self.client.PUT(update_alertrule_path, json=alertrule, headers=headers)

    async def get_rule_group(self, folder_uid, group_uid):
        """
        :param folder_uid:
        :param group_uid:
        :param disable_provenance:
        :return:
        """
        get_rule_group_path = "/v1/provisioning/folder/%s/rule-groups/%s" % (folder_uid, group_uid)
        return await self.client.GET(get_rule_group_path)

    async def update_rule_group(self, folder_uid, group_uid, alertrule_group, disable_provenance=False):
        """
        :param folder_uid:
        :param group_uid:
        :param alertrule_group:
        :return:
        """
        headers = {}
        if disable_provenance:
            headers["X-Disable-Provenance"] = "true"
        update_rule_group_path = "/v1/provisioning/folder/%s/rule-groups/%s" % (folder_uid, group_uid)
        return await self.client.PUT(update_rule_group_path, json=alertrule_group, headers=headers)

    async def delete_alertrule(self, alertrule_uid):
        """
        @param alertrule_uid:
        @param alertrule:
        @return:
        """

        delete_alertrule_path = "/v1/provisioning/alert-rules/%s" % alertrule_uid
        return await self.client.DELETE(delete_alertrule_path)

    async def get_contactpoints(self, name=None):
        """
        Gets all contact points, optionally filtering by name.
        @return:
        """
        path = "/v1/provisioning/contact-points"
        params = {}
        if name:
            params = {"name": name}
        return await self.client.GET(path, params=params)

    async def create_contactpoint(self, contactpoint, disable_provenance=False):
        """
        Creates single contact point
        @param contactpoint:
        @param disable_provenance:
        @return:
        """
        headers = {}
        if disable_provenance:
            headers["X-Disable-Provenance"] = "true"
        create_contactpoint_path = "/v1/provisioning/contact-points"
        return await self.client.POST(create_contactpoint_path, json=contactpoint, headers=headers)

    async def update_contactpoint(self, contactpoint_uid, contactpoint):
        """
        Updates existing contact point
        @param contactpoint_uid:
        @param contactpoint:
        @return:
        """
        update_contactpoint_path = "/v1/provisioning/contact-points/%s" % contactpoint_uid
        return await self.client.PUT(update_contactpoint_path, json=contactpoint)

    async def delete_contactpoint(self, contactpoint_uid):
        """
        Deletes existing contactpoint
        @param contactpoint_uid:
        @return:
        """
        delete_contactpoint_path = "/v1/provisioning/contact-points/%s" % contactpoint_uid
        return await self.client.DELETE(delete_contactpoint_path)

    async def get_notification_policy_tree(self):
        """
        Gets notification policy tree
        @return:
        """
        get_notification_policy_tree_path = "/v1/provisioning/policies"
        return await self.client.GET(get_notification_policy_tree_path)

    async def set_notification_policy_tree(self, notification_policy_tree, disable_provenance=False):
        """
        Sets notification policy tree
        @param notification_policy_tree:
        @param disable_provenance:
        @return:
        """
        headers = {}
        if disable_provenance:
            headers["X-Disable-Provenance"] = "true"
        set_notification_policy_tree_path = "/v1/provisioning/policies"
        return await self.client.PUT(set_notification_policy_tree_path, json=notification_policy_tree, headers=headers)

    async def delete_notification_policy_tree(self):
        """
        Removes notification policy tree
        @return:
        """
        delete_notification_policy_tree_path = "/v1/provisioning/policies"
        return await self.client.DELETE(delete_notification_policy_tree_path)

    async def get_mute_timings(self):
        """
        Gets all mute timings
        @return:
        """
        get_mute_timings_path = "/v1/provisioning/mute-timings"
        return await self.client.GET(get_mute_timings_path)

    async def get_mute_timing(self, mutetiming_name):
        """
        Gets single mute timing
        @return:
        """
        get_mute_timing_path = "/v1/provisioning/mute-timings/%s" % mutetiming_name
        return await self.client.GET(get_mute_timing_path)

    async def create_mute_timing(self, mutetiming, disable_provenance=False):
        """
        Creates single mute timing
        @param mutetiming:
        @param disable_provenance:
        @return:
        """
        headers = {}
        if disable_provenance:
            headers["X-Disable-Provenance"] = "true"
        create_mute_timing_path = "/v1/provisioning/mute-timings"
        return await self.client.POST(create_mute_timing_path, json=mutetiming, headers=headers)

    async def update_mute_timing(self, mutetiming_name, mutetiming):
        """
        Updates existing mute timing
        @return:
        """
        update_mute_timing_path = "/v1/provisioning/mute-timings/%s" % mutetiming_name
        return await self.client.PUT(update_mute_timing_path, json=mutetiming)

    async def delete_mute_timing(self, mutetiming_name):
        """
        Deletes single mute timing
        @return:
        """
        delete_mute_timing_path = "/v1/provisioning/mute-timings/%s" % mutetiming_name
        return await self.client.DELETE(delete_mute_timing_path)

    async def get_templates(self):
        """
        Gets all templates
        @return:
        """
        get_templates_path = "/v1/provisioning/templates"
        return await self.client.GET(get_templates_path)

    async def get_template(self, template_name):
        """
        Gets single template
        @param template_name:
        @return:
        """
        get_template_path = "/v1/provisioning/templates/%s" % template_name
        return await self.client.GET(get_template_path)

    async def create_or_update_template(self, template_name, template, disable_provenance=False):
        """
        Creates or updates (if given template_name exists) template
        @param template_name:
        @param template:
        @param disable_provenance:
        @return:
        """
        headers = {}
        if disable_provenance:
            headers["X-Disable-Provenance"] = "true"
        create_template_path = "/v1/provisioning/templates/%s" % template_name
        return await self.client.PUT(create_template_path, json=template, headers=headers)

    async def delete_template(self, template_name):
        """
        Deletes template
        @param template_name:
        @param template:
        @return:
        """
        create_template_path = "/v1/provisioning/templates/%s" % template_name
        return await self.client.DELETE(create_template_path)
