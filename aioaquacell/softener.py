"""Represents all properties of a softener device."""
import string
from datetime import datetime
from typing import cast


class Softener:
    def __init__(self, data):
        self.halfLevelNotificationEnabled: bool = data["halfLevelNotificationEnabled"]
        self.thresholds: dict = data["thresholds"]
        self.on_boarding_date: datetime = datetime.utcfromtimestamp(cast(float, data["on_boarding_date"]) / 1000)
        self.dummy: string = data["dummy"]
        self.name: string = data["name"]
        self.ssn: string = data["ssn"]
        self.dsn: string = data["dsn"]
        self.salt: Salt = Salt(data["salt"])
        self.wifiLevel: string = data["wifiLevel"]
        self.fwVersion: string = data["fwVersion"]
        self.lastUpdate = datetime.utcfromtimestamp(cast(float, data["lastUpdate"]) / 1000)
        self.battery: int = data["battery"]
        self.lidInPlace: bool = data["lidInPlace"]
        self.buzzerNotificationEnabled: bool = data["buzzerNotificationEnabled"]
        self.brand: string = data["brand"]
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
        self.address: string = data["address"]
        self.postcode: string = data["postcode"]
        self.country: string = data["country"]


class Dealer:
    def __init__(self, data):
        self.website: string = data["website"]
        self.dealerId: string = data["dealerId"]
        self.shop: dict = data["shop"]
        self.name: string = data["name"]
        self.support: dict = data["support"]
