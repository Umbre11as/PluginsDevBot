from .repository import ShopRepository
from .model import Plugin, PathUnion
from typing import List
from decimal import Decimal
from sqlalchemy import create_engine, Column, String, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()

class PluginDB(Base):
    __tablename__ = 'plugins'
    
    name = Column(String(255), primary_key=True)
    description = Column(Text)
    file_path = Column(String(500))
    price = Column(Numeric(10, 2), nullable=False, default=0.00)

class DatabaseShopRepository(ShopRepository):
    def __init__(self, db_type: str = 'sqlite', db_name: str = 'shop.db', host: str = 'localhost', port: int = 3306, user: str = 'root', password: str = ''):
        type = db_type.lower()
        if type == 'h2':
            self.engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
        elif type == 'sqlite':
            self.engine = create_engine(f'sqlite:///{db_name}', connect_args={'check_same_thread': False})
        elif type == 'mysql':
            self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}')
        else:
            raise ValueError(f'Unsupported database type: {db_type}')
        
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def add_plugin(self, name: str, description: str, file_path: PathUnion, price: Decimal):
        with self.SessionLocal() as session:
            existing = session.query(PluginDB).filter_by(name=name).first()
            if existing:
                existing.description = description
                existing.file_path = str(file_path)
                existing.price = price
            else:
                plugin_db = PluginDB(name=name, description=description, file_path=str(file_path), price=price)
                session.add(plugin_db)
            
            session.commit()
    
    def remove_plugin(self, name: str):
        with self.SessionLocal() as session:
            plugin = session.query(PluginDB).filter_by(name=name).first()
            if plugin:
                session.delete(plugin)
                session.commit()
    
    def get_plugin(self, name: str) -> Plugin:
        with self.SessionLocal() as session:
            plugin_db = session.query(PluginDB).filter_by(name=name).first()
            if plugin_db:
                return Plugin(name=plugin_db.name, description=plugin_db.description, file_path=plugin_db.file_path, price=Decimal(str(plugin_db.price)))

            return None
    
    def list_plugins(self) -> List[Plugin]:
        with self.SessionLocal() as session:
            plugins_db = session.query(PluginDB).all()
            return [
                Plugin(name=plugin.name, description=plugin.description, file_path=plugin.file_path, price=Decimal(str(plugin.price))) for plugin in plugins_db
            ]
