import math
import random
from faker import Faker

faker = Faker("pt_PT")

TIPOS_INSTITUICAO = [
    "Associação", "Fundação", "Cooperativa", "IPSS",
    "Misericórdia", "Mutualidade", "ONG", "Federação",
    "União", "Centro Social",
]

# Centro de Vila do Conde — local onde o painel vai ser testado.
# Enviesa-se a escolha de localidades para garantir que a lista do painel
# tem pedidos suficientes dentro do raio de cobertura.
VILA_DO_CONDE_LAT = 41.3522
VILA_DO_CONDE_LNG = -8.7497
VILA_DO_CONDE_RAIO_KM = 25
PROB_LOCAL_PROXIMA = 0.80


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2)
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _localidades_proximas_vdc(localidades: list[dict]) -> list[dict]:
    return [
        loc for loc in localidades
        if _haversine_km(
            VILA_DO_CONDE_LAT, VILA_DO_CONDE_LNG,
            loc.get("_latitude") or 0, loc.get("_longitude") or 0,
        ) <= VILA_DO_CONDE_RAIO_KM
    ]


def _gerar_nipc() -> str:
    """
    Gera um NIPC com primeiro dígito 5 (entidade pública) ou 9 (pessoa coletiva)
    """
    prefixo = random.choice(
        ["5", "5", "5", "5", "9", "9", "9", "9", "9", "9", "9"])
    prefixo = random.choices(
        ["5", "9"],
        weights=[35, 65],  # aplicar peso ao prefixo de cada nif
        k=1
    )[0]
    return prefixo + faker.numerify("########")


def generate_instituicao(localidades: list[dict], localidades_proximas: list[dict] | None = None) -> dict:
    """
    Gera um registo de Instituição.
    Herda codigo_postal de uma localidade gerada e usa as suas
    coordenadas internas (_latitude, _longitude) para geo_latitude/geo_longitude.
    Enviesa para localidades próximas de Vila do Conde quando disponíveis.
    """
    if localidades_proximas and random.random() < PROB_LOCAL_PROXIMA:
        loc = random.choice(localidades_proximas)
    else:
        loc = random.choice(localidades)
    nipc = _gerar_nipc()

    return {
        "nif_nipc": nipc,
        "codigo_postal": loc["codigo_postal"],
        "geo_latitude": loc["_latitude"],
        "geo_longitude": loc["_longitude"],
        "url_comprovativo_estatuto": f"https://docs.instituicoes.pt/{nipc}.pdf",
    }


def generate_instituicoes(n: int = 50, localidades: list[dict] = None) -> list[dict]:
    """
    Gera n instituições únicas (por NIPC)
    Requer a lista de localidades geradas para obter coordenadas reais
    """
    if not localidades:
        raise ValueError("É necessário fornecer uma lista de localidades.")

    resultados = []
    nipcs_vistos = set()

    localidades_proximas = _localidades_proximas_vdc(localidades)
    print(
        f"A gerar {n} instituições "
        f"(~{int(PROB_LOCAL_PROXIMA * 100)}% perto de Vila do Conde, "
        f"{len(localidades_proximas)} localidades dentro de {VILA_DO_CONDE_RAIO_KM}km)...\n"
    )

    while len(resultados) < n:
        registo = generate_instituicao(localidades, localidades_proximas)
        nipc = registo["nif_nipc"]

        if nipc in nipcs_vistos:
            continue

        nipcs_vistos.add(nipc)
        resultados.append(registo)

    # Fixture de teste — NIF fixo para o Postman chain
    if "599999998" not in nipcs_vistos:
        resultados.append({
            "nif_nipc": "599999998",
            "codigo_postal": localidades[0]["codigo_postal"],
            "geo_latitude": 41.3522,
            "geo_longitude": -8.7497,
            "url_comprovativo_estatuto": "https://docs.instituicoes.pt/599999998.pdf",
        })

    print(f"  Concluído! {len(resultados)} instituições geradas.\n")
    return resultados
