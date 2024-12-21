"""Represents all properties of a softener device."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import cast


@dataclass
class Softener:
    """Softener object."""

    def __init__(self, data):
        self.name: str = data["name"]
        self.ssn: str = data["ssn"]
        self.dsn: str = data["dsn"]
        self.salt: Salt = Salt(data["salt"])
        self.lid_place: bool = data["lidInPlace"]
        self.brand: str = data["brand"]
        self.diagnostics: Diagnostics = Diagnostics(data)


@dataclass
class Salt:
    """Salt object."""

    def __init__(self, data):
        self.left_percent: int = data.get("leftPercent", 0)
        self.right_percent: int = data.get("rightPercent", 0)
        self.left_days: int = data["leftDays"]
        self.right_days: int = data["rightDays"]
        self.left_blocks: int = data["leftBlocks"]
        self.right_blocks: int = data["rightBlocks"]
        self.days_left: int = data["daysLeft"]


@dataclass
class Diagnostics:
    """Holds diagnostic data."""

    def __init__(self, data):
        self.wifi_level: str = data["wifiLevel"]
        self.fw_version: str = data["fwVersion"]
        self.last_update = datetime.fromtimestamp(
            cast(float, data["lastUpdate"]) / 1000, tz=timezone.utc
        )
        self.battery: int = data["battery"]
