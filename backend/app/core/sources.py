from loguru import logger

import csv, requests, os

from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
from elasticsearch.connection import create_ssl_context
from elasticsearch.exceptions import NotFoundError
from app.core.config import settings


BUCKET_PREFIX= os.getenv('BUCKET_PREFIX','')
POOL_CONNS  = int(os.getenv('POOL_CONNS',200))
POOL_MAX    = int(os.getenv('POOL_MAX',200))
MAX_RETRIES = int(os.getenv('MAX_RETRIES',2))
MINIO_TIMEOUT= int(os.getenv('MINIO_TIMEOUT',30))

def get_es(es_url, es_user, es_pass):
        import ssl
        from elasticsearch.connection import create_ssl_context
        ssl_context = create_ssl_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        es = Elasticsearch([es_url], 
                            connection_class=RequestsHttpConnection, 
                            http_auth=(es_user, es_pass),
                            timeout=60, 
                            max_retries=10, 
                            maxsize=2, 
                            retry_on_timeout=True,
                            verify_certs=False,
                            ssl_context=ssl_context,
                            use_ssl=False)
        
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
        for uf in ufs_to_install:
            source_files.append(
                {
                    "cands": "sources/candidaturas/consulta_cand_2020_%s.csv" % uf,
                    "receitas": "sources/prestacao_candidaturas/receitas_candidatos_2020_%s.csv" % uf
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

        for src in source_files:
            cands_source_dict = get_source_dict(src["cands"])
            logger.info(">>> Carregando recurso: %s" % src["cands"])
            for item in cands_source_dict:
                if cands_source_dict.index(item) > cands_index_count:
                    item["id"] = item["SQ_CANDIDATO"]
                    send_to_elastic(
                        item,
                        "2020_cands",
                        settings.ES_URL,
                        "", ""
                    )

            receitas_source_dict = get_source_dict(src["receitas"])
            logger.info(">>> Carregando recurso: %s" % src["receitas"])
            for item in receitas_source_dict:
                if receitas_source_dict.index(item) > receitas_index_count:
                    item["id"] = item["NR_RECIBO_DOACAO"]
                    send_to_elastic(
                        item,
                        "2020_receitas",
                        settings.ES_URL,
                        "", ""
                    )
            
