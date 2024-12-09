"""Represents all properties of a softener device."""
from datetime import datetime, timezone
from typing import cast


class Softener:
    """ Softener object. """
    def __init__(self, data):
        self.half_level_notification_enabled: bool = data["halfLevelNotificationEnabled"]
        self.on_boarding_date: datetime = datetime.fromtimestamp(
            cast(float, data["on_boarding_date"]) / 1000, tz=timezone.utc)
        self.name: str = data["name"]
        self.ssn: str = data["ssn"]
        self.dsn: str = data["dsn"]
        self.salt: Salt = Salt(data["salt"])
        self.wifi_level: str = data["wifiLevel"]
        self.fw_version: str = data["fwVersion"]
        self.last_update = datetime.fromtimestamp(cast(float, data["lastUpdate"]) / 1000, tz=timezone.utc)
        self.battery: int = data["battery"]
        self.lid_place: bool = data["lidInPlace"]
        self.buzzer_notification_enabled: bool = data["buzzerNotificationEnabled"]
        self.brand: str = data["brand"]


class Salt:
    """ Salt object. """  
    def __init__(self, data):
        self.left_percent: int = data.get("leftPercent", 0)
        self.right_percent: int = data.get("rightPercent", 0)
        self.left_days: int = data["leftDays"]
        self.right_days: int = data["rightDays"]
        self.left_blocks: int = data["leftBlocks"]
        self.right_blocks: int = data["rightBlocks"]
        self.days_left: int = data["daysLeft"]
