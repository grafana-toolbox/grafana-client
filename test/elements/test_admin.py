import unittest

import requests_mock

from grafana_client import GrafanaApi


class AdminTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_settings(self, m):
        m.get(
            "http://localhost/api/admin/settings",
            json={
                "DEFAULT": {"app_mode": "production"},
                "analytics": {"google_analytics_ua_id": "", "reporting_enabled": "false"},
                "auth.anonymous": {"enabled": "true", "org_name": "Main Org.", "org_role": "Viewer"},
                "auth.basic": {"enabled": "false"},
                "auth.github": {
                    "allow_sign_up": "false",
                    "allowed_domains": "",
                    "allowed_organizations": "",
                    "api_url": "https://api.github.com/user",
                    "auth_url": "https://github.com/login/oauth/authorize",
                    "client_id": "some_id",
                    "client_secret": "************",
                    "enabled": "false",
                    "scopes": "user:email,read:org",
                    "team_ids": "",
                    "token_url": "https://github.com/login/oauth/access_token",
                },
                "auth.google": {
                    "allow_sign_up": "false",
                    "allowed_domains": "",
                    "api_url": "https://www.googleapis.com/oauth2/v1/userinfo",
                    "auth_url": "https://accounts.google.com/o/oauth2/auth",
                    "client_id": "some_client_id",
                    "client_secret": "************",
                    "enabled": "false",
                    "scopes": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",  # noqa:E501
                    "token_url": "https://accounts.google.com/o/oauth2/token",
                },
                "auth.ldap": {"config_file": "/etc/grafana/ldap.toml", "enabled": "false"},
                "auth.proxy": {
                    "auto_sign_up": "true",
                    "enabled": "false",
                    "header_name": "X-WEBAUTH-USER",
                    "header_property": "username",
                },
                "dashboards.json": {"enabled": "false", "path": "/var/lib/grafana/dashboards"},
                "database": {
                    "host": "127.0.0.1:0000",
                    "name": "grafana",
                    "password": "************",
                    "path": "grafana.db",
                    "ssl_mode": "disable",
                    "type": "sqlite3",
                    "user": "root",
                },
                "emails": {"templates_pattern": "emails/*.html", "welcome_email_on_sign_up": "false"},
                "log": {"buffer_len": "10000", "level": "Info", "mode": "file"},
                "log.console": {"level": ""},
                "log.file": {
                    "daily_rotate": "true",
                    "file_name": "",
                    "level": "",
                    "log_rotate": "true",
                    "max_days": "7",
                    "max_lines": "1000000",
                    "max_lines_shift": "28",
                    "max_size_shift": "",
                },
                "paths": {"data": "/tsdb/grafana", "logs": "/logs/apps/grafana"},
                "security": {
                    "admin_password": "************",
                    "admin_user": "admin",
                    "cookie_remember_name": "grafana_remember",
                    "cookie_username": "grafana_user",
                    "disable_gravatar": "false",
                    "login_remember_days": "7",
                    "secret_key": "************",
                },
                "server": {
                    "cert_file": "",
                    "cert_key": "",
                    "domain": "mygraf.com",
                    "enable_gzip": "false",
                    "enforce_domain": "false",
                    "http_addr": "127.0.0.1",
                    "http_port": "0000",
                    "protocol": "http",
                    "root_url": "%(protocol)s://%(domain)s:%(http_port)s/",
                    "router_logging": "true",
                    "data_proxy_logging": "true",
                    "static_root_path": "public",
                },
                "session": {
                    "cookie_name": "grafana_sess",
                    "cookie_secure": "false",
                    "gc_interval_time": "",
                    "provider": "file",
                    "provider_config": "sessions",
                    "session_life_time": "86400",
                },
                "smtp": {
                    "cert_file": "",
                    "enabled": "false",
                    "from_address": "admin@grafana.localhost",
                    "from_name": "Grafana",
                    "ehlo_identity": "dashboard.example.com",
                    "host": "localhost:25",
                    "key_file": "",
                    "password": "************",
                    "skip_verify": "false",
                    "user": "",
                },
                "users": {
                    "allow_org_create": "true",
                    "allow_sign_up": "false",
                    "auto_assign_org": "true",
                    "auto_assign_org_role": "Viewer",
                },
            },
        )
        admin = self.grafana.admin.settings()
        self.assertEqual(admin["users"]["allow_org_create"], "true")

    @requests_mock.Mocker()
    def test_stats(self, m):
        m.get(
            "http://localhost/api/admin/stats",
            json={
                "users": 2,
                "orgs": 1,
                "dashboards": 4,
                "snapshots": 2,
                "tags": 6,
                "datasources": 1,
                "playlists": 1,
                "stars": 2,
                "alerts": 2,
                "activeUsers": 1,
            },
        )
        stats = self.grafana.admin.stats()
        self.assertEqual(len(stats), 10)

    @requests_mock.Mocker()
    def test_create_user(self, m):
        m.post("http://localhost/api/admin/users", json={"id": 5, "message": "User created"})
        user = self.grafana.admin.create_user(
            {"name": "User", "email": "user@graf.com", "login": "user", "password": "userpassword"}
        )
        self.assertEqual(user["message"], "User created")

    @requests_mock.Mocker()
    def test_change_user_password(self, m):
        m.put("http://localhost/api/admin/users/2/password", json={"message": "User password updated"})
        user = self.grafana.admin.change_user_password(user_id=2, password="password")
        self.assertEqual(user["message"], "User password updated")

    @requests_mock.Mocker()
    def test_change_user_permissions(self, m):
        m.put("http://localhost/api/admin/users/2/permissions", json={"message": "User permissions updated"})
        user = self.grafana.admin.change_user_permissions(user_id=2, is_grafana_admin=True)
        self.assertEqual(user["message"], "User permissions updated")

    @requests_mock.Mocker()
    def test_delete_user(self, m):
        m.delete("http://localhost/api/admin/users/2", json={"message": "User deleted"})
        user = self.grafana.admin.delete_user(user_id=2)
        self.assertEqual(user["message"], "User deleted")

    @requests_mock.Mocker()
    def test_pause_all_alerts(self, m):
        m.post(
            "http://localhost/api/admin/pause-all-alerts",
            json={"state": "Paused", "message": "alert paused", "alertsAffected": 1},
        )
        pause = self.grafana.admin.pause_all_alerts(pause="True")
        self.assertEqual(pause["message"], "alert paused")
