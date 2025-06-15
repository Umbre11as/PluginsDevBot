from database import Base
from sqlalchemy import Column, String, Text, Numeric

class PluginDB(Base):
    __tablename__ = 'plugins'
    
    name = Column(String(255), primary_key=True)
    description = Column(Text)
    file_path = Column(String(500))
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
