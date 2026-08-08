from sqlalchemy.orm import sessionmaker
from backend.database.connection import engine

SessionLocal = sessionmaker(autoflush=False,
                            autocommit=False,
                            bind=engine)

