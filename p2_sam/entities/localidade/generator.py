import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import math
import time
from faker import Faker
import pgeocode

faker = Faker("pt_PT")
geo   = pgeocode.Nominatim("PT")


def generate_localidade() -> dict | None:
    """
    Gera um registo de Localidade válido.
    Sem latitude/longitude — essas pertencem a Instituicao e Negocio.

    Schema (tabela Localidade):
        codigo_postal VARCHAR(45) PK
        concelho      VARCHAR(45)
        pais          VARCHAR(45)
        n_porta       VARCHAR(45)
        rua           VARCHAR(45)
    """
    cp = faker.postcode()
    r  = geo.query_postal_code(cp)

    if math.isnan(r["latitude"]) or math.isnan(r["longitude"]):
        return None

    return {
        "codigo_postal" : cp,
        "rua"           : faker.street_name()[:45],
        "freguesia"     : r["place_name"][:45]  if isinstance(r["place_name"],  str) else None,
        "concelho"      : r["county_name"][:45] if isinstance(r["county_name"], str) else None,
        "distrito"      : r["state_name"][:45]  if isinstance(r["state_name"],  str) else None,
        "n_porta"       : faker.numerify("##"),
        "pais"          : "Portugal",
        # guardamos lat/lon internamente para uso por outras entidades
        # estes campos NÃO existem na tabela Localidade da BD
        "_latitude"     : round(float(r["latitude"]),  8),
        "_longitude"    : round(float(r["longitude"]), 8),
    }


def generate_localidades(n: int = 100) -> list[dict]:
    """
    Gera n localidades únicas e válidas com progresso e estatísticas.
    """
    resultados     = []
    tentativas     = 0
    codigos_vistos = set()
    inicio         = time.time()

    print(f"A gerar {n} localidades válidas...\n")

    while len(resultados) < n:
        tentativas += 1
        registo = generate_localidade()

        if registo is None:
            continue

        cp = registo["codigo_postal"]
        if cp in codigos_vistos:
            continue

        codigos_vistos.add(cp)
        resultados.append(registo)

    total = time.time() - inicio
    minutos, segundos = divmod(total, 60)
    print(f"\n{chr(9472) * 50}")
    print(f"  Concluído!")
    print(f"  Registos válidos : {len(resultados)}")
    print(f"  Total tentativas : {tentativas}")
    if minutos > 0:
        print(f"  Tempo total      : {int(minutos)}m {segundos:.1f}s")
    else:
        print(f"  Tempo total      : {segundos:.1f}s")
    print(f"{chr(9472) * 50}\n")
    return resultados
def strip_internal_fields(localidades: list[dict]) -> list[dict]:
    """Remove campos gerados para outras entidades (_latitude, _longitude) antes de exportar."""
    return [{k: v for k, v in loc.items() if not k.startswith("_")} for loc in localidades]