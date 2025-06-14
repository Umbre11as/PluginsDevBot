from abc import ABC, abstractmethod
from typing import Optional
from ..types.payment import PaymentRequest, PaymentResponse, PaymentNotification
from api.log import get_logger

class PaymentProvider(ABC):
    @abstractmethod
    async def create_payment(self, request: PaymentRequest) -> PaymentResponse:
        raise NotImplementedError()
    
    @abstractmethod
    async def verify_notification(self, notification: PaymentNotification) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_payment_status(self, payment_id: str) -> str:
        raise NotImplementedError()

class PaymentHandler(ABC):
    @abstractmethod
    async def on_payment_success(self, notification: PaymentNotification, user_id: int, order_id: str):
        raise NotImplementedError()
    
    @abstractmethod
    async def on_payment_failed(self, notification: PaymentNotification, user_id: int, order_id: str):
        raise NotImplementedError()

class PaymentManager:
    def __init__(self, provider: PaymentProvider):
        self.provider = provider
        self.handlers: list[PaymentHandler] = []
    
    def add_handler(self, handler: PaymentHandler):
        self.handlers.append(handler)
    
    async def create_payment(self, request: PaymentRequest) -> PaymentResponse:
        response = await self.provider.create_payment(request)
        return response
    
    async def process_notification(self, notification: PaymentNotification):
        is_valid = await self.provider.verify_notification(notification)
        if not is_valid:
            return
        
        if notification.label:
            label_parts = notification.label.split('_', 1)
            
            if len(label_parts) >= 2:
                try:
                    user_id = int(label_parts[0])
                    order_id = label_parts[1]
                    
                    if not notification.unaccepted:
                        for handler in self.handlers:
                            await handler.on_payment_success(notification, user_id, order_id)
                    else:
                        for handler in self.handlers:
                            await handler.on_payment_failed(notification, user_id, order_id)
                except ValueError as exception:
                    get_logger().error(exception)
