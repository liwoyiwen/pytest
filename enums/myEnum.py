from enum import Enum


class Feature(Enum):
    portraitUpgrade = 0
    appCircle = 2
    sms = 3
    balance = 4
    flowPackage = 12


class PaymentChannel(Enum):
    ali_pay = 0
    yin_lian = 2
    balance = 4
    office_gift = 5
    open_gift = 6
    person_charge = 7
    person_refund = 8
