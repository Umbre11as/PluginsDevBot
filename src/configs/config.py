from dataclasses import dataclass

@dataclass
class Database:
    type: str
    path: str
    host: str
    port: int
    user: str
    password: str

@dataclass
class Config:
    database: Database
