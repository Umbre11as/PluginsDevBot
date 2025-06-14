from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Button:
    text: str
    callback_data: Optional[str] = None

@dataclass
class KeyboardRow:
    buttons: List[Button]

class Keyboard(ABC):
    def __init__(self):
        self.rows: List[KeyboardRow] = []
    
    def add_row(self, *buttons: Button):
        self.rows.append(KeyboardRow(list(buttons)))
        return self
    
    def add_button(self, text: str, callback_data: Optional[str] = None):
        if not self.rows:
            self.rows.append(KeyboardRow([]))
        
        self.rows[-1].buttons.append(Button(text, callback_data))
        return self
    
    @abstractmethod
    def build(self):
        raise NotImplementedError()

class InlineKeyboard(Keyboard):
    @abstractmethod
    def build(self):
        raise NotImplementedError()

class ReplyKeyboard(Keyboard):
    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = False):
        super().__init__()
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
    
    @abstractmethod
    def build(self):
        raise NotImplementedError()
