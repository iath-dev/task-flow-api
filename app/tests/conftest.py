import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.api.deps import get_db
from app.core.config import settings

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})

@pytest.fixture(scope="session", autouse=True)
def setup_database(engine):
    settings.DATABASE_URL = "sqlite:///./test.db"
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()
    os.remove("./test.db")

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c