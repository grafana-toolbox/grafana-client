import asyncio
import socket

from grafana_client import AsyncGrafanaApi
from grafana_client.client import GrafanaClientError

try:
    from unittest import IsolatedAsyncioTestCase
except ImportError:
    pass
else:

    class TestAsync(IsolatedAsyncioTestCase):
        async def test_basic_async_client(self):
            try:
                sock = socket.create_connection(("play.grafana.org", 80), timeout=1)
            except (ConnectionRefusedError, socket.gaierror, TimeoutError):
                self.skipTest("Test requires a WAN access to play.grafana.org")
            else:
                sock.close()

            async def fetch_dashboard(async_client, uid):
                return await async_client.dashboard.get_dashboard(uid)

            grafana = AsyncGrafanaApi(host="play.grafana.org")

            await grafana.connect()

            version = await grafana.version

            self.assertTrue(version != "" and "." in version)

            folders = await grafana.folder.get_all_folders()

            self.assertTrue(isinstance(folders, list))
            self.assertTrue(len(folders) >= 4)

            tasks = []

            for folder in folders[:2]:
                if folder["id"] > 0:  # someone created an entry with a negative id...
                    dashboards = await grafana.search.search_dashboards(folder_uids=[folder["uid"]])
                    for dashboard in dashboards[:4]:
                        tasks.append(fetch_dashboard(grafana, dashboard["uid"]))

            results = await asyncio.gather(*tasks)

            self.assertEqual(len(results), 4)
            self.assertTrue(all(isinstance(r, dict) and list(r.keys()) for r in results))

        async def test_exception_async_client(self):
            try:
                sock = socket.create_connection(("play.grafana.org", 80), timeout=1)
            except (ConnectionRefusedError, socket.gaierror, TimeoutError):
                self.skipTest("Test requires a WAN access to play.grafana.org")
            else:
                sock.close()

            grafana = AsyncGrafanaApi(host="play.grafana.org")

            await grafana.version

            with self.assertRaises(GrafanaClientError) as exc:
                await grafana.admin.change_user_password(0, "impossible")

            self.assertEqual(exc.exception.status_code, 403)
