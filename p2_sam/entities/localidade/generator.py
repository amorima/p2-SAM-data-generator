import math
import random
import time
import ssl
import pgeocode
from faker import Faker
ssl._create_default_https_context = ssl._create_unverified_context

faker = Faker("pt_PT")
geo = pgeocode.Nominatim("PT")
_valid_localidades: list[dict] | None = None    # cache de localidades validas

# O painel vai ser testado em Vila do Conde — garantir cobertura local.
VILA_DO_CONDE_LAT = 41.3522
VILA_DO_CONDE_LNG = -8.7497
VILA_DO_CONDE_RAIO_KM = 25
MIN_LOCALIDADES_PROXIMAS_VDC = 30


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2)
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _get_valid_localidades() -> list[dict]:
    """Obtem e gera localidades válidas do dataset do pgeocode"""
    global _valid_localidades

    if _valid_localidades is None:
        dados = geo._data.dropna(
            subset=["postal_code", "latitude", "longitude"]
        ).drop_duplicates(subset=["postal_code"])

        _valid_localidades = dados.to_dict("records")

    return _valid_localidades


def generate_localidade() -> dict | None:
    r = random.choice(_get_valid_localidades())
    cp = r["postal_code"]

    return {
        "codigo_postal": cp,
        "rua": faker.street_name()[:45],
        "freguesia": r["place_name"][:45] if isinstance(r["place_name"], str) else None,
        "concelho": r["county_name"][:45] if isinstance(r["county_name"], str) else None,
        "distrito": r["state_name"][:45] if isinstance(r["state_name"], str) else None,
        "n_porta": faker.numerify("###"),
        "pais": "Portugal",
        "_latitude": round(float(r["latitude"]), 8),
        "_longitude": round(float(r["longitude"]), 8),
    }


def generate_localidades(n: int = 100) -> list[dict]:
    inicio = time.time()
    validas = _get_valid_localidades()

    if n > len(validas):
        raise ValueError(
            f"Só existem {len(validas)} localidades válidas disponíveis."
        )

    # Separar localidades perto de Vila do Conde para garantir presença mínima.
    proximas_vdc = [
        v for v in validas
        if isinstance(v.get("latitude"), float) and isinstance(v.get("longitude"), float)
        and _haversine_km(VILA_DO_CONDE_LAT, VILA_DO_CONDE_LNG, v["latitude"], v["longitude"]) <= VILA_DO_CONDE_RAIO_KM
    ]
    n_proximas = min(MIN_LOCALIDADES_PROXIMAS_VDC, len(proximas_vdc), n)
    amostra_proxima = random.sample(proximas_vdc, n_proximas) if n_proximas else []

    cps_proximas = {p["postal_code"] for p in amostra_proxima}
    restantes = [v for v in validas if v["postal_code"] not in cps_proximas]
    amostra_resto = random.sample(restantes, n - n_proximas)

    amostra = amostra_proxima + amostra_resto
    random.shuffle(amostra)

    print(
        f"A gerar {n} localidades válidas "
        f"({n_proximas} garantidas até {VILA_DO_CONDE_RAIO_KM}km de Vila do Conde)...\n"
    )

    resultados = []
    for r in amostra:
        resultados.append({
            "codigo_postal": r["postal_code"],
            "rua": faker.street_name()[:45],
            "freguesia": r["place_name"][:45] if isinstance(r["place_name"], str) else None,
            "concelho": r["county_name"][:45] if isinstance(r["county_name"], str) else None,
            "distrito": r["state_name"][:45] if isinstance(r["state_name"], str) else None,
            "n_porta": faker.numerify("##"),
            "pais": "Portugal",
            "_latitude": round(float(r["latitude"]), 8),
            "_longitude": round(float(r["longitude"]), 8),
        })

    total = time.time() - inicio
    minutos, segundos = divmod(total, 60)

    print(f"\n{chr(9472) * 50}")
    print("  Concluído!")
    print(f"  Registos válidos : {len(resultados)}")
    print(f"  Total tentativas : {len(resultados)}")
    print(f"  Tempo total      : {int(minutos)}m {segundos:.1f}s" if minutos >
          0 else f"  Tempo total      : {segundos:.1f}s")
    print(f"{chr(9472) * 50}\n")

    return resultados


def strip_internal_fields(localidades: list[dict]) -> list[dict]:
    """Remove campos internos antes de exportar a tabela Localidade."""
    return [
        {k: v for k, v in localidade.items() if not k.startswith("_")}
        for localidade in localidades
    ]
