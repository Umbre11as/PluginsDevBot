from dataclasses import dataclass
from typing import List

@dataclass
class Keyboard:
    make_order: str
    shop: str
    support: str
    my_orders: str

@dataclass
class Shop:
    empty: str
    entry: List[str]
    message: str
    button: str
    buy_button: str
    not_found: str
    pay_button: str
    payment_info: List[str]
    plugin_not_found_after_payment: List[str]
    success_payment: List[str]
    caption: str
    file_not_found: List[str]
    payment_failed: List[str]

@dataclass
class MakeOrder:
    version: str
    tech_task: str

@dataclass
class StatusTranslation:
    not_paid: str
    not_started: str
    in_process: str
    ready: str

@dataclass
class MyOrders:
    empty: str
    button: str

@dataclass
class OrderButtons:
    hurry_up: str
    support: str

@dataclass
class Order:
    message: List[str]
    buttons: OrderButtons

@dataclass
class AdminKeyboard:
    shop: str
    orders: str
    back: str

@dataclass
class AdminShop:
    welcome: str

@dataclass
class Admin:
    keyboard: AdminKeyboard
    shop: AdminShop
    welcome: str
    wrong_password: str
    enter_password: str
    blocked: str

@dataclass
class Messages:
    start: List[str]
    keyboard: Keyboard
    shop: Shop
    make_order: MakeOrder
    status: StatusTranslation
    my_orders: MyOrders
    order: Order
    admin: Admin
