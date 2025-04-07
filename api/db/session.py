from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from api.core.deps import settings

if settings.PROD == True:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        future=True,
        
    )
else:
    engine = create_engine(
        "sqlite:///./test.db",
   
        pool_pre_ping=True,
        future=True,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
