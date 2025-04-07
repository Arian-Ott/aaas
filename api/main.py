# api/main.py
from api.core.deps import settings  # Import settings first to access settings.PROD
from api.core.logging import setup_logging

# Set up logging using settings.PROD
setup_logging(prod=settings.PROD)

from fastapi import FastAPI
from api.routes import user, security, roles
from api.db.session import Base, engine
import logging

app = FastAPI(
    debug=not settings.PROD,
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

def startup():
    if not settings.PROD:
        logging.warning("🚧 Running in development mode, using SQLite database. 🚧")
        logging.warning("🚧 Dropping all DB 🚧")
        logging.info("Creating database tables.")
        logging.info("Database URL: %s", settings.DATABASE_URL)
        Base.metadata.drop_all(bind=engine)
    else:
        logging.info("Creating database tables.")
        logging.info("Database URL: %s", settings.DATABASE_URL)
        logging.warning("ℹ️ Running in Production mode ℹ️")
    Base.metadata.create_all(bind=engine)

app.add_event_handler("startup", startup)
app.include_router(user.router)
app.include_router(security.sapi_router)
app.include_router(roles.router)