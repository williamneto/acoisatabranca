from loguru import logger

import csv, requests, os, time

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from app.core.config import settings


BUCKET_PREFIX= os.getenv('BUCKET_PREFIX','')
POOL_CONNS  = int(os.getenv('POOL_CONNS',200))
POOL_MAX    = int(os.getenv('POOL_MAX',200))
MAX_RETRIES = int(os.getenv('MAX_RETRIES',2))
MINIO_TIMEOUT= int(os.getenv('MINIO_TIMEOUT',30))

def get_es(es_url, es_user, es_pass):
        es = Elasticsearch(es_url, basic_auth=(es_user, es_pass) )
        
        return es

def send_to_elastic(data, es_index, es_url, es_user, es_pass):
    es = get_es(es_url, es_user, es_pass)

    sess = requests.Session()
    sess.verify = False
    adapter = requests.adapters.HTTPAdapter(pool_connections=POOL_CONNS, pool_maxsize=POOL_MAX, max_retries=MAX_RETRIES)
    sess.mount('http://', adapter)

    try:
        es.update(
            index=es_index,
            id=data["id"], 
            body={'doc': data, 'doc_as_upsert': True}
        )

    except Exception as e:
        logger.error('==================================')
        logger.error('ELASTIC UPSERT ERROR==============')
        logger.error('==================================')
        logger.error(e)

def es_scroll(es, index, body, scroll, size, **kw):
    page = es.search(index=index, body=body, scroll=scroll, size=size, **kw)
    scroll_id = page['_scroll_id']
    hits = page['hits']['hits']
    while len(hits):
        yield hits
        page = es.scroll(scroll_id=scroll_id, scroll=scroll)
        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']    

def install_sources():
    skip_install = settings.SKIP_INSTALL 
    ufs_to_install = settings.UFS_INSTALL.split(",")
    logger.info("UFs a instalar: %s " % ufs_to_install)
    es = get_es(settings.ES_URL, "", "")
    
    if skip_install:
        logger.info(">>> Pulando instalação de recursos")
    else:
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

        source_files = []
        if len(ufs_to_install) > 0:
            for uf in ufs_to_install:
                source_files.append(
                    {
                        "cands": "sources/candidaturas/consulta_cand_2020_%s.csv" % uf,
                        "receitas": "sources/prestacao_candidaturas/receitas_candidatos_2020_%s.csv" % uf,
                        "receitas_partidos": "sources/prestacao_orgaos/receitas_orgaos_partidarios_2020_%s.csv" % uf,
                        "despesas_partidos": "sources/prestacao_orgaos/despesas_contratadas_orgaos_partidarios_2020_%s.csv" % uf
                    }
                )
        
        def get_source_dict(filepath):
            source_dicts = []
            with open(filepath, encoding='latin-1') as infile:
                logger.info(">>> Mapeando arquivo %s" % filepath)
                reader = csv.reader(infile, delimiter=';')
                i = 1
                header = []
                for row in reader:
                    if i == 1:
                        header = row
                        i += 1
                    else:
                        data = {
                            head: row[header.index(head)] for head in header
                        }
                        source_dicts.append(data)
                        
                        i += 1
            
            return source_dicts

        def install_cands():
            for src in source_files:
                cands_source_dict = get_source_dict(src["cands"])
                logger.info(">>> Carregando recurso: %s" % src["cands"])
                for item in cands_source_dict:
                    # if cands_source_dict.index(item) > cands_index_count:
                    item["id"] = item["SQ_CANDIDATO"]
                    send_to_elastic(
                        item,
                        "2020_cands",
                        settings.ES_URL,
                        "", ""
                    )

        def install_cands_receitas():
            for src in source_files:
                receitas_source_dict = get_source_dict(src["receitas"])
                logger.info(">>> Carregando recurso: %s" % src["receitas"])
                for item in receitas_source_dict:
                    # if receitas_source_dict.index(item) > receitas_index_count:
                    item["id"] = "%s_%s" % (item["SQ_RECEITA"], item["DT_RECEITA"])
                    send_to_elastic(
                        item,
                        "2020_receitas",
                        settings.ES_URL,
                        "", ""
                    )
        
        def install_receitas_partidos():
            for src in source_files:
                receitas_partidos_source_dict = get_source_dict(src["receitas_partidos"])
                logger.info(">>> Carregando recurso: %s" % src["receitas_partidos"])
                for item in receitas_partidos_source_dict:
                    # if receitas_partidos_source_dict.index(item) > receitas_partidos_index_count:
                    item["id"] = "%s_%s" % (item["SQ_RECEITA"], item["DT_RECEITA"])
                    send_to_elastic(
                        item,
                        "2020_receitas_partidos",
                        settings.ES_URL,
                        "", ""
                    )

        def install_despesas_partidos():
            for src in source_files:
                despesas_partidos_source_dict = get_source_dict(src["despesas_partidos"])
                logger.info(">>> Carregando recurso: %s" % src["despesas_partidos"])
                for item in despesas_partidos_source_dict:
                    # if despesas_source_dict.index(item) > despesas_index_count:
                    item["id"] = "%s_%s" % (item["SQ_DESPESA"], item["DT_DESPESA"])
                    send_to_elastic(
                        item,
                        "2020_despesas_partidos",
                        settings.ES_URL,
                        "", ""
                    )

        if settings.INSTALL_CANDS:
            install_cands()
            install_cands_receitas()

        if settings.INSTALL_PARTIDOS:
            install_receitas_partidos()
            install_despesas_partidos()

def analize_despesas_partidos():
    es = get_es(
        settings.ES_URL, "", ""
    )

    body = {
        "query": {
            "match_all": {}
        }
    }
    partidos_doacoes_cands = {}
    for despesas_hits in es_scroll(es, "2020_despesas_partidos", body,"2m", 40):
        for despesa in despesas_hits:
            despesa = despesa["_source"]
            if despesa["DS_ORIGEM_DESPESA"] == "Doações financeiras a outros candidatos/partidos":
                despesa_key = "%s_%s" % ( despesa["SG_PARTIDO"], despesa["NM_MUNICIPIO_FORNECEDOR"])
                if despesa_key in partidos_doacoes_cands:
                    partidos_doacoes_cands[despesa_key].append(
                        despesa
                    )
                else:
                    partidos_doacoes_cands[despesa_key] = [despesa]
    
    for doacao_key in partidos_doacoes_cands:
        destino_doacao = {
            "SG_PARTIDO": "",
            "NM_MUNICIPIO": "%s" % doacao_key.split("_")[1],
            "total": 0.0,
            "brancs": 0.0,
            "brancs_eleitos": 0.0,
            "brancs_eleitos_percent": 0,
            "prets": 0.0,
            "prets_eleitos": 0.0,
            "prets_eleitos_percent": 0
        }
        doacoes_partido = partidos_doacoes_cands[doacao_key]
        for doacao in doacoes_partido:
            destino_doacao["SG_PARTIDO"] = doacao["SG_PARTIDO"]
            destino_doacao["total"] += float(doacao["VR_DESPESA_CONTRATADA"].replace(",", "."))
            body = {"query": {
                "term": {
                    "SQ_CANDIDATO.keyword": doacao["SQ_CANDIDATO_FORNECEDOR"] 
                }
            }}
            search = es.search(
                index="2020_cands",
                body=body
            )
            if len(search["hits"]["hits"]) > 0:
                cand = search["hits"]["hits"][0]["_source"]
                if cand["DS_COR_RACA"] == "PARDA" or cand["DS_COR_RACA"] == "PRETA":
                    destino_doacao["prets"] += float(doacao["VR_DESPESA_CONTRATADA"].replace(",", "."))
                    if cand["DS_SIT_TOT_TURNO"] == "ELEITO POR QP" or cand["DS_SIT_TOT_TURNO"] == "ELEITO POR MÉDIA" or cand["DS_SIT_TOT_TURNO"] == "ELEITO":
                        destino_doacao["prets_eleitos"] += float(doacao["VR_DESPESA_CONTRATADA"].replace(",", "."))
                else:
                    destino_doacao["brancs"] += float(doacao["VR_DESPESA_CONTRATADA"].replace(",", "."))
                    if cand["DS_SIT_TOT_TURNO"] == "ELEITO POR QP" or cand["DS_SIT_TOT_TURNO"] == "ELEITO POR MÉDIA" or cand["DS_SIT_TOT_TURNO"] == "ELEITO":
                        destino_doacao["brancs_eleitos"] += float(doacao["VR_DESPESA_CONTRATADA"].replace(",", "."))
            
        destino_doacao["id"] = doacao_key
        destino_doacao["brancs_eleitos_percent"] = (  destino_doacao["brancs_eleitos"] / destino_doacao["total"] ) * 100
        destino_doacao["prets_eleitos_percent"] = (  destino_doacao["prets_eleitos"] / destino_doacao["total"] ) * 100
        send_to_elastic(
            destino_doacao,
            "2020_partidos_doacoes_cands",
            settings.ES_URL, "", ""
        )



def analize_sources():
    es = get_es(
        settings.ES_URL, "", ""
    )
    cidades = settings.CTS_INSTALL.split(",")
    
    def save_cidade_partido(cand):
        send_to_elastic(
            {
                "id": "%s_%s" % (cand["NM_UE"], cand["SG_UF"]),
                "SG_UF": cand["SG_UF"],
                "NM_UE": cand["NM_UE"]
            },
            "ues_mapping",
            settings.ES_URL, "", ""
        )

        send_to_elastic(
            {
                "id": cand["SG_PARTIDO"],
                "SG_PARTIDO": cand["SG_PARTIDO"],
                "NM_PARTIDO": cand["NM_PARTIDO"],
                "NR_PARTIDO": cand["NR_PARTIDO"]
            },
            "partidos_mapping",
            settings.ES_URL, "", ""
        )
    
    def analisa_receitas(cand):
        logger.info(">> Analizando receitas candidato %s" % cand["NM_URNA_CANDIDATO"])
        body={'query': {'term': {'SQ_CANDIDATO.keyword': cand["SQ_CANDIDATO"]}}}

        receita_total = 0.0
        receita_partido = 0.0
        for receitas in es_scroll(es, "2020_receitas", body, "2m", 20):
            for receita in receitas:
                receita_total += float(receita["_source"]["VR_RECEITA"].replace(",","."))
                if receita["_source"]["DS_ORIGEM_RECEITA"] == "Recursos de partido político":
                    receita_partido += float(receita["_source"]["VR_RECEITA"].replace(",","."))

        if receita_partido == 0:
            partido_percent = 0
        else:
            quociente = receita_partido / receita_total
            partido_percent = quociente * 100

        analise_obj = {
            "id": cand["SQ_CANDIDATO"],
            "SQ_CANDIDATO": cand["SQ_CANDIDATO"],
            "NM_URNA_CANDIDATO": cand["NM_URNA_CANDIDATO"],
            "DS_CARGO": cand["DS_CARGO"],
            "DS_COMPOSICAO_COLIGACAO": cand["DS_COMPOSICAO_COLIGACAO"],
            "DS_DETALHE_SITUACAO_CAND": cand["DS_DETALHE_SITUACAO_CAND"],
            "NM_UE": cand["NM_UE"],
            "SG_PARTIDO": cand["SG_PARTIDO"],
            "DS_COR_RACA": cand["DS_COR_RACA"],
            "DS_GENERO": cand["DS_GENERO"],
            "DS_SIT_TOT_TURNO": cand["DS_SIT_TOT_TURNO"],
            "DS_GRAU_INSTRUCAO": cand["DS_GRAU_INSTRUCAO"],
            "DS_OCUPACAO": cand["DS_OCUPACAO"],
            "RECEITA_TOTAL": receita_total,
            "RECEITA_PARTIDO": receita_partido,
            "PERCENT_RECEITA_PARTIDO": partido_percent
        }
        send_to_elastic(
            analise_obj,
            "2020_analise",
            settings.ES_URL,
            "", ""
        )

        save_cidade_partido(cand)
        time.sleep(0.2)
    
    if len(cidades) > 0:
        for cidade in cidades:
            body={'query': {'term': {'NM_UE.keyword': cidade}}}
            cidade_cands = []
            for cands in es_scroll(es, "2020_cands", body, '2m', 20):
                for cand in cands:
                    cidade_cands.append(cand["_source"])

            for cand in cidade_cands:  
                analisa_receitas(cand)
                time.sleep(0.2)
    else:
        body = {
            "query": {
                "match_all": {}
            }
        }
        cidade_cands = []
        for cands in es_scroll(es, "2020_cands", body, '2m', 20):
            for cand in cands:
                cidade_cands.append(cand["_source"])

        for cand in cidade_cands:  
            analisa_receitas(cand)
            time.sleep(0.2)