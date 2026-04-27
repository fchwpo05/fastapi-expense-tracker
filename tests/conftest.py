import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import get_db


#TEST database
SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:rules%401234@localhost:5432/expense_tracker_test"
)

# Test engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Test session factory
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        try: 
            yield test_client
        finally: 
            app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    client.post(
        "/api/v1/users/signup",
        json={
            "email": "auth@example.com",
            "name": "Auth User",
            "password": "secret123"
        }
    )

    response = client.post(
        "/api/v1/users/login",
        json={
            "email": "auth@example.com",
            "name": "Auth User",
            "password": "secret123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }