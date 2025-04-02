from fastapi import FastAPI
from api.routes import user
from api.routes import security
from api.db.session import Base, engine

app = FastAPI()


def startup():
    if os.getenv("ENV") != "production":
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    

app.add_event_handler("startup", startup)
app.include_router(user.router)
app.include_router(security.sapi_router)
