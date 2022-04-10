
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT

from app.core.config import settings
from app.database.mongodb import connect_db,close_db
from app.core.sources import install_sources


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", close_db)
app.add_event_handler("startup", install_sources)


@AuthJWT.load_config
def get_config():
    return settings


