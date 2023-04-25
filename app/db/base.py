from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()


database_url = settings.DATABASE_URL
metadata = MetaData()
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(engine)
