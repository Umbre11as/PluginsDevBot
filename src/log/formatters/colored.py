from logging import Formatter
import re

class ColoredFormatter(Formatter):
    COLORS = {
        'DEBUG': '\033[93m',
        'WARNING': '\033[33m', 
        'INFO': '\033[92m',
        'ERROR': '\033[91m',
    }
    RESET = '\033[0m'

    def format(self, record):
        timestamp = self.formatTime(record, '%H:%M').lstrip('0')
        levelname = record.levelname
        color = self.COLORS.get(levelname, '')
        level_colored = f'{color}{levelname.lower()}{self.RESET}'

        prefix = f'[{timestamp}] [{level_colored}]'
        padding = ' ' * (20 - len(self._strip_ansi(prefix)))

        return f'{prefix}{padding}{record.getMessage()}'

    def _strip_ansi(self, text):
        return re.sub(r'\x1b\[[0-9;]*m', '', text)
