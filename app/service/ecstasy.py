import asyncio
import os
from typing import Optional, Dict, List

import aiohttp


class EcstasyConnector:
    _url = os.getenv("ECSTASY_URL")
    _login = os.getenv("ECSTASY_LOGIN")
    _password = os.getenv("ECSTASY_PASSWORD")

    def __init__(self):
        self._raw_session: Optional[aiohttp.ClientSession] = None
        self._tokens: Dict[str, str] = {}

    async def request(self, method: str, url: str, **kwargs):
        """
        Функция выполняет HTTP-запрос с обработкой аутентификации.
        """
        if not self._tokens:
            await self._do_auth()

        kwargs["headers"] = self._add_token(kwargs.get("headers"))

        resp = await self._session.request(method, self._url + url, **kwargs)
        if resp.status in [401, 403]:
            await self._do_auth()
            kwargs["headers"] = self._add_token(kwargs.get("headers"))
            resp = await self._session.request(method, self._url + url, **kwargs)
        return resp

    def _add_token(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        if headers is None:
            headers = {}
        headers.update({"Authorization": f"Bearer {self._tokens.get('access')}"})
        return headers

    async def _do_auth(self):
        # Для начало проверяем, имеется ли возможность обновить access token через refresh token
        if self._tokens.get("refresh"):
            resp = await self._session.post(
                self._url + "/api/token/refresh",
                json={"refresh": self._tokens.get("refresh")},
            )
            print("DO AUTH", resp.status)
            if resp.status == 200:
                self._tokens = await resp.json()
                resp.close()
                return
            else:
                resp.close()

        # Если не удалось обновить через refresh token
        resp = await self._session.post(
            self._url + "/api/token",
            json={"username": self._login, "password": self._password},
        )
        if resp.status == 200:
            self._tokens = await resp.json()
        resp.close()

    @property
    def _session(self) -> aiohttp.ClientSession:
        if self._raw_session is None:
            self._raw_session = aiohttp.ClientSession(
                headers={"Content-Type": "application/json"}
            )
        return self._raw_session

    @_session.setter
    def _session(self, value):
        self._raw_session = value

    async def __aenter__(self) -> "EcstasyConnector":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None


class EcstasyService:
    connector: EcstasyConnector = EcstasyConnector()

    async def get_interfaces_workload(
        self, devices_names: List[str]
    ) -> List[Dict[str, int]]:
        async with self.connector as conn:
            tasks = [
                self._get_interfaces_workload(connection=conn, device_name=devices_name)
                for devices_name in devices_names
            ]
            return await asyncio.gather(*tasks)

    @staticmethod
    async def _get_interfaces_workload(connection, device_name: str) -> Dict[str, int]:
        resp = await connection.request(
            "get", f"/device/api/workload/interfaces/{device_name}"
        )
        if resp.status == 200:
            return await resp.json()
        return {}


ecstasy_service = EcstasyService()
