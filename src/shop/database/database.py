from ..model import Plugin
from .repository import ShopRepository
from .orm import PluginDB
from database import SessionLocal
from typing import List
from decimal import Decimal

class DatabaseShopRepository(ShopRepository):
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def add_plugin(self, name: str, description: str, file_path, price: Decimal):
        with self._session_factory() as session:
            exists = session.query(PluginDB).filter_by(name=name).first()
            if exists:
                exists.description = description
                exists.file_path   = str(file_path)
                exists.price       = price
            else:
                session.add(PluginDB(
                    name=name,
                    description=description,
                    file_path=str(file_path),
                    price=price
                ))
            
            session.commit()

    def remove_plugin(self, name: str):
        with self._session_factory() as session:
            plugin = session.query(PluginDB).filter_by(name=name).first()
            if plugin:
                session.delete(plugin)
                session.commit()

    def get_plugin(self, name: str) -> Plugin:
        with self._session_factory() as session:
            p = session.query(PluginDB).filter_by(name=name).first()
            if not p:
                return None
            
            return Plugin(name=p.name, description=p.description, file_path=p.file_path, price=p.price)

    def list_plugins(self) -> List[Plugin]:
        with self._session_factory() as session:
            rows = session.query(PluginDB).all()
            return [
                Plugin(name=r.name, description=r.description, file_path=r.file_path, price=r.price)
                for r in rows
            ]
