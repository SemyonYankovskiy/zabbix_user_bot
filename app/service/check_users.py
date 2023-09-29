from typing import Dict
from datetime import datetime


class AffectedSubscribersChecker:

    async def calculate_affected_subscribers(self, from_datetime: datetime) -> None:
        pass

    # def get_affected_subscribers(self):
    def get_affected_subscribers(self) -> Dict[str, int]:
        return {
            "device1": 13,
            "device2": 20,
        }


