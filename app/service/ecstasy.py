import asyncio
import os
from typing import Dict, List

import aiohttp


class EcstasyService:
    def __init__(self, base_url: str = "", token: str = ""):
        self._base_url = base_url
        self._token = token
        self.headers = {"Authorization": f"Token {self._token}"}
        self._session = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(base_url=self._base_url, headers=self.headers)
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get_interfaces_workload(
        self, devices_names: List[str]
    ) -> List[Dict[str, int]]:
        async with self.session as conn:
            tasks = [
                self._get_interfaces_workload(connection=conn, device_name=devices_name)
                for devices_name in devices_names
            ]
            return await asyncio.gather(*tasks)

    @staticmethod
    async def _get_interfaces_workload(connection, device_name: str) -> Dict[str, int]:
        resp = await connection.get(f"/api/v1/devices/workload/interfaces/{device_name}")
        if resp.status == 200:
            return await resp.json()
        return {}


ecstasy_service = EcstasyService(base_url=os.environ["ECSTASY_URL"], token=os.environ["ECSTASY_TOKEN"])
