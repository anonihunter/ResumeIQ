from backend.core.settings import settings
from sqlalchemy import create_engine

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=settings.debug, pool_pre_ping=True)
