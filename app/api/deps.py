from sqlalchemy.orm import Session, sessionmaker

from app.db.session import get_engine

def get_db() -> Session:
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()