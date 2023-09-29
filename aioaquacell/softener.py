"""Represents all properties of a softener device."""


class Softener:
    def __init__(self, data):
        self.halfLevelNotificationEnabled = data["halfLevelNotificationEnabled"]
        self.thresholds = data["thresholds"]
        self.on_boarding_date = data["on_boarding_date"]
        self.dummy = data["dummy"]
        self.name = data["name"]
        self.ssn = data["ssn"]
        self.dsn = data["dsn"]
        self.salt: Salt = data["salt"]
        self.wifiLevel = data["wifiLevel"]
        self.fwVersion = data["fwVersion"]
        self.lastUpdate = data["lastUpdate"]
        self.battery = data["battery"]
        self.lidInPlace = data["lidInPlace"]
        self.buzzerNotificationEnabled = data["buzzerNotificationEnabled"]
        self.brand = data["brand"]
        self.numberOfPeople = data["numberOfPeople"]
        self.location: Location = data["location"]
        self.dealer: Dealer = data["dealer"]


class Salt:
    def __init__(self, data):
        self.leftPercent = data["leftPercent"]
        self.rightPercent = data["rightPercent"]
        self.leftDays = data["leftDays"]
        self.rightDays = data["rightDays"]
        self.leftBlocks = data["leftBlocks"]
        self.rightBlocks = data["rightBlocks"]
        self.daysLeft = data["daysLeft"]


class Location:
    def __init__(self, data):
        self.address = data["address"]
        self.postcode = data["postcode"]
        self.country = data["country"]


class Dealer:
    def __init__(self, data):
        self.website = data["website"]
        self.dealerId = data["dealerId"]
        self.shop = data["shop"]
        self.name = data["name"]
        self.support = data["support"]
