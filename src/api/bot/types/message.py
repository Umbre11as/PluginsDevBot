from dataclasses import dataclass
from typing import Optional

@dataclass
class Document:
    file_id: str
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

@dataclass
class Message:
    sender_id: int
    text: str
    document: Optional[Document] = None
