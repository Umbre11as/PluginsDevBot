class Placeholder:
    def __init__(self, text: str):
        self.text = text
        self.placeholders = {}

    def place(self, key: str, value: str):
        self.placeholders[key] = value
        return self

    def build(self) -> str:
        text = self.text
        for key, value in Placeholder.items():
            text = text.replace(key, value)
        
        return text
