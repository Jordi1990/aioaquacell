"""Represents all properties of a softener device."""
from datetime import datetime, timezone
from typing import cast


class Softener:
    def __init__(self, data):
        self.halfLevelNotificationEnabled: bool = data["halfLevelNotificationEnabled"]
        self.thresholds: dict = data["thresholds"]
        self.on_boarding_date: datetime = datetime.fromtimestamp(
            cast(float, data["on_boarding_date"]) / 1000, tz=timezone.utc)
        self.dummy: string = data["dummy"]
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
        self.numberOfPeople: int = data["numberOfPeople"]
        self.location: Location = Location(data["location"])
        self.dealer: Dealer = Dealer(data["dealer"])


class Salt:
    def __init__(self, data):
        self.leftPercent: int = data.get("leftPercent", 0)
        self.rightPercent: int = data.get("rightPercent", 0)
        self.leftDays: int = data["leftDays"]
        self.rightDays: int = data["rightDays"]
        self.leftBlocks: int = data["leftBlocks"]
        self.rightBlocks: int = data["rightBlocks"]
        self.daysLeft: int = data["daysLeft"]


class Location:
    def __init__(self, data):
        self.address: str = data["address"]
        self.postcode: str = data["postcode"]
        self.country: str = data["country"]


class Dealer:
    def __init__(self, data):
        self.website: str = data["website"]
        self.dealerId: str = data["dealerId"]
        self.shop: dict = data["shop"]
        self.name: str = data["name"]
        self.support: dict = data["support"]
