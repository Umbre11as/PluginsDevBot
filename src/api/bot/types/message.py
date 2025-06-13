from dataclasses import dataclass

@dataclass
class Message:
    sender_id: int
    text: str
