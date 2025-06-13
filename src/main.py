from log import get_logger
from configs import ConfigurationManager
from dataclasses import dataclass
from typing import List

logger = get_logger()

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
    button: str

@dataclass
class MakeOrder:
    version: str
    tech_task: str

@dataclass
class Status:
    not_paid: str
    not_started: str
    in_process: str
    ready: str

@dataclass
class MyOrders:
    empty: str
    button: str

@dataclass
class Buttons:
    hurry_up: str
    support: str

@dataclass
class Order:
    message: List[str]
    buttons: Buttons

@dataclass
class Messages:
    start: List[str]
    keyboard: Keyboard
    shop: Shop
    make_order: MakeOrder
    status: Status
    my_orders: MyOrders
    order: Order

manager = ConfigurationManager('configs')
messages = manager.load(Messages, 'messages.yml')

def main():
    logger.info('Code seems to be correct')
    print(messages)

if __name__ == '__main__':
    main()
