"""Represents all properties of a softener device."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import cast


@dataclass
class Salt:
    """Salt object."""

    left_percent: int
    right_percent: int
    left_days: int
    right_days: int
    left_blocks: int
    right_blocks: int
    days_left: int

    @classmethod
    def from_dict(cls, data: dict) -> Salt:
        """Create from API salt dict."""
        return cls(
            left_percent=data.get("leftPercent", 0),
            right_percent=data.get("rightPercent", 0),
            left_days=data["leftDays"],
            right_days=data["rightDays"],
            left_blocks=data["leftBlocks"],
            right_blocks=data["rightBlocks"],
            days_left=data["daysLeft"],
        )


@dataclass
class Diagnostics:
    """Holds diagnostic data."""

    wifi_level: str
    fw_version: str
    last_update: datetime
    battery: int

    @classmethod
    def from_dict(cls, data: dict) -> Diagnostics:
        """Create from API softener dict."""
        return cls(
            wifi_level=data["wifiLevel"],
            fw_version=data["fwVersion"],
            last_update=datetime.fromtimestamp(
                cast(float, data["lastUpdate"]) / 1000, tz=timezone.utc
            ),
            battery=data["battery"],
        )


@dataclass
class Softener:
    """Softener object."""

    name: str
    ssn: str
    dsn: str
    salt: Salt
    lid_place: bool
    brand: str
    diagnostics: Diagnostics

    @classmethod
    def from_dict(cls, data: dict) -> Softener:
        """Create from API softener dict."""
        return cls(
            name=data["name"],
            ssn=data["ssn"],
            dsn=data["dsn"],
            salt=Salt.from_dict(data["salt"]),
            lid_place=data["lidInPlace"],
            brand=data["brand"],
            diagnostics=Diagnostics.from_dict(data),
        )
