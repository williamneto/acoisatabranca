
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from elasticsearch.exceptions import NotFoundError
from loguru import logger

from app.core.config import settings
from app.database.mongodb import connect_db,close_db
from app.core.sources import install_sources, get_es, analize_sources


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
if not settings.SKIP_INSTALL:
    app.add_event_handler("startup", install_sources)

if not settings.SKIP_ANALIZE:
    app.add_event_handler("startup", analize_sources)

@app.get("/")
async def get_status():
    es = get_es(
        settings.ES_URL, "", ""
    )
    cands_index_count = 0
    try:
        search_for_index = es.count(
            index="2020_cands"
        )
        cands_index_count = search_for_index["count"]
        
    except NotFoundError:
        cands_index_count = 0
    
    receitas_index_count = 0
    try:
        search_for_index = es.count(
            index="2020_receitas"
        )
        receitas_index_count = search_for_index["count"]
        
    except NotFoundError:
        receitas_index_count = 0
    
    return {
        "cands_index": cands_index_count,
        "receitas_index": receitas_index_count
    }

@app.get(
    "/cidade/"
)
async def get_cidade_data(cidade: str):
    es = get_es(
        settings.ES_URL, "", ""
    )
    
    cands = es.search(
        index="2020_cands",
        body={'query': {'match': {'NM_UE': cidade}}},
        size=999
    )
    return cands

@AuthJWT.load_config
def get_config():
    return settings


