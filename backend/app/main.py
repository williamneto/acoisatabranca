
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from elasticsearch.exceptions import NotFoundError
from loguru import logger

from app.core.config import settings
from app.database.mongodb import connect_db,close_db
from app.core.sources import es_scroll, install_sources, get_es, analize_sources, analize_despesas_partidos


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

if settings.ANALIZE_PARTIDOS:
    app.add_event_handler("startup", analize_despesas_partidos)

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
async def get_cidade_data(cidade: str, partido : str = None):
    es = get_es(
        settings.ES_URL, "", ""
    )

    all_cands = []
    cands_prets = []
    cands_prets_eleitos = []
    all_cands_eleitos = []

    if partido:
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                'SG_PARTIDO.keyword': partido
                            },
                        }, 
                        {
                            "match": {
                                'NM_UE.keyword': cidade
                            },
                        }
                    ]
                }
            }
        }
        
        partido_doacoes = []
        for doacoes_hits in es_scroll(es, "2020_partidos_doacoes_cands", body, "2m", 40):

            for hit in doacoes_hits:
                doacao = hit["_source"]
                
                doacao["brancs_eleitos_percent"] = "%s %%" % str(round(doacao["brancs_eleitos_percent"], 2))
                doacao["prets_eleitos_percent"] = "%s %%" % str(round(doacao["prets_eleitos_percent"], 2))
                partido_doacoes.append(
                    doacao
                )
    else:
        body = {'query': {'match': {'NM_UE.keyword': cidade}}}
        partido_doacoes = []

    for cands_hits in es_scroll(es, "2020_analise", body, "2m", 40):
        for cand in cands_hits:
            cand = cand["_source"]
            all_cands.append(cand)
            if cand["DS_COR_RACA"] == "PRETA" or cand["DS_COR_RACA"] == "PERTA":
                cands_prets.append(cand)
                if cand["DS_SIT_TOT_TURNO"] == "ELEITO POR QP" or cand["DS_SIT_TOT_TURNO"] == "ELEITO POR MÉDIA" or cand["DS_SIT_TOT_TURNO"] == "ELEITO":
                    cands_prets_eleitos.append(cand)
            
            if cand["DS_SIT_TOT_TURNO"] == "ELEITO POR QP" or cand["DS_SIT_TOT_TURNO"] == "ELEITO POR MÉDIA" or cand["DS_SIT_TOT_TURNO"] == "ELEITO":
                all_cands_eleitos.append(cand)

    if len(cands_prets) > 0 and len(all_cands) > 0:
        percent_cands_prets = (  len(cands_prets) / len(all_cands) ) * 100
    else:
        percent_cands_prets = 0
    
    if len(cands_prets_eleitos) > 0 and len(all_cands) > 0:
        percent_eleitos_prets =  (len(cands_prets_eleitos) / len(all_cands_eleitos)) * 100
    else:
        percent_eleitos_prets = 0

    return {
        "total_cands": len(all_cands),
        "all_cands_eleitos": len(all_cands_eleitos),
        "cands_prets": len(cands_prets),
        "cands_prets_eleitos": len(cands_prets_eleitos),
        "percent_cands_prets": "%s %%" % str(round(percent_cands_prets, 2)),
        "percent_eleitos_prets": "%s %%" % str(round(percent_eleitos_prets, 2)),
        "partido_doacoes": partido_doacoes
    }

@app.get(
    "/cidades/"
)
async def get_avaliable_cidades():
    es = get_es(
        settings.ES_URL, "", ""
    )
    body = {
        "query": {
            "match_all": {}
        }
    }

    

    cidades = []
    for cidade_hits in es_scroll(es, "ues_mapping", body, "2m", 40):
        for cidade in cidade_hits:
            cidades.append(
                cidade["_source"]
            )
    
    return cidades

@app.get(
    "/partidos/"
)
async def get_avaliable_partidos():
    es = get_es(
        settings.ES_URL, "", ""
    )
    body = {
        "query": {
            "match_all": {}
        }
    }   

    partidos = []
    for partido_hits in es_scroll(es, "partidos_mapping", body, "2m", 40):
        for partido in partido_hits:
            partidos.append(
                partido["_source"]
            )
    
    return partidos

@AuthJWT.load_config
def get_config():
    return settings


