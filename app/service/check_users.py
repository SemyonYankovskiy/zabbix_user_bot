import os
from typing import Dict
from datetime import datetime

from .zabbix import ZabbixService
from .ecstasy import ecstasy_service

_zabbix_group_names = os.getenv("ZABBIX_GROUP_NAMES", "").split(",")


async def get_affected_subscribers(from_datetime: datetime) -> Dict[str, int]:
    devices = {}
    device_names = await ZabbixService.get_unavailable_devices_names(
        from_group_names=_zabbix_group_names,
        time_from=from_datetime,
    )

    stats = await ecstasy_service.get_interfaces_workload(device_names)
    for device_names, workload in zip(device_names, stats):
        devices[device_names] = workload.get("abons_up")

    return devices
