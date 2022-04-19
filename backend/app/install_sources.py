from app.core.config import settings
from app.core.sources import es_scroll, install_sources, get_es, analize_sources, analize_despesas_partidos

if not settings.SKIP_INSTALL:
    install_sources()

if not settings.SKIP_ANALIZE:
    analize_sources()

if settings.ANALIZE_PARTIDOS:
    analize_despesas_partidos()