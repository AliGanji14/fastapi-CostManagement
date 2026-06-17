from dotenv import load_dotenv
load_dotenv()
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from core.database import Base, get_db
from users.models import UserModel
from auth.jwt_auth import generate_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
def test_user(test_db):
    """Create a test user."""
    user = UserModel(username="testuser")
    user.set_password("testpassword")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def anon_client(test_db):
    """Create an unauthenticated test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
def authenticated_client(client, test_user):
    """Create an authenticated test client."""
    access_token = generate_access_token(test_user.id)
    client.cookies.set("access_token", access_token)
    return client
