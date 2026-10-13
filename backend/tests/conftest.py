
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from backend.core.settings import settings
from backend.database.base import Base
from backend.database.dependencies import get_db
from backend.app.main import app
from backend.models.user import User  # Register User table in metadata


# Always target the separate test database.
test_database_url = make_url(settings.database_url).set(
    database="resumeiq_test"
)

if test_database_url.database != "resumeiq_test":
    raise RuntimeError("Refusing to run tests on a non-test database")

test_engine = create_engine(test_database_url, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=test_engine
)


@pytest.fixture
def client():
    # Create tables only in resumeiq_test.
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        db.close()
        Base.metadata.drop_all(bind=test_engine)
