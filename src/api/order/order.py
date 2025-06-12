from enum import Enum, auto

class OrderType(Enum):
    NOT_PAID = auto(),
    NOT_STARTED = auto(),
    IN_PROCESS = auto(),
    READY = auto()

class Order:
    def __init__(self, id: int, type: OrderType):
        self.id = id
        self.type = type

class OrdersRepository:
    pass

class OrdersService:
    pass
