from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

Base = declarative_base()

engine = create_engine(
    'sqlite:///database.db',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
