from typing import Dict
from datetime import datetime

from .zabbix import ZabbixService
from .ecstasy import ecstasy_service


class AffectedSubscribersChecker:
    def __init__(self):
        self._devices: Dict[str, int] = {}

    async def calculate_affected_subscribers(self, from_datetime: datetime) -> None:
        device_names = await ZabbixService.get_unavailable_devices_names(
            from_group_names=["Доступ"], time_from=from_datetime
        )

        stats = await ecstasy_service.get_interfaces_workload(device_names)
        for device_names, workload in zip(device_names, stats):
            self._devices[device_names] = workload.get("abons_up")

    def get_affected_subscribers(self) -> Dict[str, int]:
        return self._devices
