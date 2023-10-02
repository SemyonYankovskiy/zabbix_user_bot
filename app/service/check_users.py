from typing import Dict
from datetime import datetime

from .zabbix import ZabbixService
from .ecstasy import ecstasy_service


async def get_affected_subscribers(from_datetime: datetime) -> Dict[str, int]:
    devices = {}
    device_names = await ZabbixService.get_unavailable_devices_names(
        from_group_names=["Доступ"], time_from=from_datetime
    )

    stats = await ecstasy_service.get_interfaces_workload(device_names)
    for device_names, workload in zip(device_names, stats):
        devices[device_names] = workload.get("abons_up")

    return devices
