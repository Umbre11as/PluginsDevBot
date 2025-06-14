from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
from decimal import Decimal

class PaymentStatus(Enum):
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class PaymentMethod(Enum):
    WALLET = 'PC'
    CARD = 'AC'

@dataclass
class PaymentItem:
    id: str
    name: str
    price: Decimal
    quantity: int = 1
    
    @property
    def total_price(self) -> Decimal:
        return self.price * self.quantity

@dataclass
class PaymentRequest:
    items: list[PaymentItem]
    user_id: int
    order_id: str
    success_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @property
    def total_amount(self) -> Decimal:
        return sum(item.total_price for item in self.items)

@dataclass
class PaymentResponse:
    payment_id: str
    payment_url: str
    amount: Decimal
    status: PaymentStatus
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class PaymentNotification:
    operation_id: str
    amount: Decimal
    currency: str
    datetime: str
    sender: str
    label: str
    notification_type: str
    codepro: bool
    sha1_hash: str
    unaccepted: bool = False
    test_notification: bool = False
