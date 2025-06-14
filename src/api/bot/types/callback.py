from dataclasses import dataclass

@dataclass
class CallbackQuery:
    id: str
    from_user_id: int
    data: str
    message_id: int
