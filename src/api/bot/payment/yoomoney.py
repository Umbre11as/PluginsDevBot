import hashlib
from decimal import Decimal
from typing import Optional
from ...bot.payment.provider import PaymentProvider
from ...bot.types.payment import PaymentRequest, PaymentResponse, PaymentNotification, PaymentStatus

class YooMoneyProvider(PaymentProvider):
    def __init__(self, wallet_id: str, notification_secret: str, success_url: Optional[str] = None):
        self.wallet_id = wallet_id
        self.notification_secret = notification_secret
        self.success_url = success_url
        self.base_url = 'https://yoomoney.ru/quickpay/confirm'
    
    async def create_payment(self, request: PaymentRequest) -> PaymentResponse:
        label = f'{request.user_id}_{request.order_id}'
        payment_url = self._build_payment_url(
            amount=request.total_amount,
            label=label,
            success_url=request.success_url or self.success_url
        )
        
        return PaymentResponse(
            payment_id=label,
            payment_url=payment_url,
            amount=request.total_amount,
            status=PaymentStatus.PENDING,
            metadata=request.metadata
        )
    
    def _build_payment_url(self, amount: Decimal, label: str, success_url: Optional[str] = None) -> str:
        params = [
            f'receiver={self.wallet_id}',
            'quickpay-form=button',
            f'sum={amount}',
            f'label={label}'
        ]
        
        if success_url:
            params.append(f'successURL={success_url}')
        
        url = f'{self.base_url}?' + '&'.join(params)
        return url
    
    async def verify_notification(self, notification: PaymentNotification) -> bool:
        hash_string = (
            f'{notification.notification_type}&'
            f'{notification.operation_id}&'
            f'{notification.amount}&'
            f'{notification.currency}&'
            f'{notification.datetime}&'
            f'{notification.sender}&'
            f'{str(notification.codepro).lower()}&'
            f'{self.notification_secret}&'
            f'{notification.label}'
        )
        
        calculated_hash = hashlib.sha1(hash_string.encode('utf-8')).hexdigest()
        is_valid = calculated_hash == notification.sha1_hash
        
        return is_valid
    
    async def get_payment_status(self, payment_id: str) -> str:
        return PaymentStatus.PENDING.value
