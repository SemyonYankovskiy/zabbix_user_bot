import os
from datetime import datetime
from typing import Optional, List

import aiohttp
from aiozabbix import ZabbixAPI


class ZabbixConnector:
    _user = os.getenv("ZABBIX_API_LOGIN")
    _password = os.getenv("ZABBIX_API_PASSWORD")
    _url = os.getenv("ZABBIX_API_URL")

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._zbx: Optional[ZabbixAPI] = None

    async def __aenter__(self) -> ZabbixAPI:
        self._session = aiohttp.ClientSession()
        self._zbx = ZabbixAPI(server=self._url, client_session=self._session)
        await self._zbx.login(self._user, self._password)
        return self._zbx

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._zbx.user.logout()
        if self._session and not self._session.closed:
            await self._session.close()


class ZabbixService:
    zabbix_connector = ZabbixConnector

    @classmethod
    async def get_unavailable_devices_names(
        cls, from_group_names: List[str], time_from: datetime
    ) -> List[str]:
        devices = []
        async with cls.zabbix_connector() as zbx:
            groups = await zbx.hostgroup.get(filter={"name": from_group_names})
            zabbix_group_ids = [gr["groupid"] for gr in groups]
            hosts_id = [
                host["hostid"]
                # Получение всех хостов в группе с заданным идентификатором группы.
                for host in await zbx.host.get(
                    groupids=zabbix_group_ids,
                    output=["hostid"],
                    filter={"status": "0"},
                )
            ]

            # Получение проблем сети из Zabbix.
            hosts_problems_list = await zbx.problem.get(
                hostids=hosts_id,
                output=["objectid"],
                time_from=time_from.timestamp(),
                filter={"name": ["Оборудование недоступно", "SWITCH DOWN"]},
            )

            print(hosts_problems_list)

            # По проблеме находим триггер, а затем название узла сети
            for problem in hosts_problems_list:
                res = await zbx.item.get(
                    triggerids=[problem["objectid"]], output=["hostid", "name"]
                )
                dev = await zbx.host.get(hostids=[res[0]["hostid"]], output=["name"])
                devices.append(dev[0]["name"])

        return devices
