"""Represents all properties of a softener device."""
from datetime import datetime, timezone
from typing import cast


class Softener:
    def __init__(self, data):
        self.halfLevelNotificationEnabled: bool = data["halfLevelNotificationEnabled"]
        self.on_boarding_date: datetime = datetime.fromtimestamp(
            cast(float, data["on_boarding_date"]) / 1000, tz=timezone.utc)
        self.name: str = data["name"]
        self.ssn: str = data["ssn"]
        self.dsn: str = data["dsn"]
        self.salt: Salt = Salt(data["salt"])
        self.wifiLevel: str = data["wifiLevel"]
        self.fwVersion: str = data["fwVersion"]
        self.lastUpdate = datetime.fromtimestamp(cast(float, data["lastUpdate"]) / 1000, tz=timezone.utc)
        self.battery: int = data["battery"]
        self.lidInPlace: bool = data["lidInPlace"]
        self.buzzerNotificationEnabled: bool = data["buzzerNotificationEnabled"]
        self.brand: str = data["brand"]


class Salt:
    def __init__(self, data):
        self.leftPercent: int = data.get("leftPercent", 0)
        self.rightPercent: int = data.get("rightPercent", 0)
        self.leftDays: int = data["leftDays"]
        self.rightDays: int = data["rightDays"]
        self.leftBlocks: int = data["leftBlocks"]
        self.rightBlocks: int = data["rightBlocks"]
        self.daysLeft: int = data["daysLeft"]
