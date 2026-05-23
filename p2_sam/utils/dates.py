import random
from datetime import datetime, timedelta

_FORMATO_SQL = "%Y-%m-%d %H:%M:%S"
_FORMATO_ISO = "%Y-%m-%dT%H:%M:%SZ"


def data_organica(
    anos: float = 2.0,
    peso_recente: float = 0.30,
    janela_recente_dias: int = 14,
    formato: str = _FORMATO_SQL,
) -> str:
    """
    Gera uma data aleatória com distribuição mista:
    - `peso_recente` (30%) das datas concentradas nos últimos `janela_recente_dias` dias
    - O restante (70%) espalhado uniformemente ao longo de `anos` anos
    Baseada na data em que o seed é executado (datetime.now()).
    """
    total_segundos = int(anos * 365 * 24 * 3600)
    recente_segundos = janela_recente_dias * 24 * 3600

    if random.random() < peso_recente:
        segundos_atras = random.uniform(0, recente_segundos)
    else:
        segundos_atras = random.uniform(0, total_segundos)

    return (datetime.now() - timedelta(seconds=segundos_atras)).strftime(formato)


def data_organica_iso(
    anos: float = 2.0,
    peso_recente: float = 0.30,
    janela_recente_dias: int = 14,
) -> str:
    return data_organica(anos, peso_recente, janela_recente_dias, _FORMATO_ISO)
