import random
from faker import Faker

faker = Faker("pt_PT")

TIPOS_INSTITUICAO = [
    "Associação", "Fundação", "Cooperativa", "IPSS",
    "Misericórdia", "Mutualidade", "ONG", "Federação",
    "União", "Centro Social",
]


def _gerar_nipc() -> str:
    """
    Gera um NIPC com primeiro dígito 5 (entidade pública) ou 9 (pessoa coletiva)
    """
    prefixo = random.choice(["5", "5", "5", "5", "9", "9", "9", "9", "9", "9", "9"])
    prefixo = random.choices(
        ["5", "9"],
        weights=[35, 65], # aplicar peso ao prefixo de cada nif 
        k=1
    )[0]
    return prefixo + faker.numerify("########")


def generate_instituicao(localidades: list[dict]) -> dict:
    """
    Gera um registo de Instituição.
    Herda codigo_postal de uma localidade gerada e usa as suas
    coordenadas internas (_latitude, _longitude) para geo_latitude/geo_longitude
    """
    loc  = random.choice(localidades)
    nipc = _gerar_nipc()
    tipo = random.choice(TIPOS_INSTITUICAO)
    nome = f"{tipo} {faker.last_name()} {faker.last_name()}"

    return {
        "nif_nipc"                  : nipc,
        "nome"                      : nome,
        "tipo"                      : tipo,
        "codigo_postal"             : loc["codigo_postal"],
        "geo_latitude"              : loc["_latitude"],
        "geo_longitude"             : loc["_longitude"],
        "url_comprovativo_estatuto" : f"https://docs.instituicoes.pt/{nipc}.pdf",
    }


def generate_instituicoes(n: int = 50, localidades: list[dict] = None) -> list[dict]:
    """
    Gera n instituições únicas (por NIPC)
    Requer a lista de localidades geradas para obter coordenadas reais
    """
    if not localidades:
        raise ValueError("É necessário fornecer uma lista de localidades.")

    resultados   = []
    nipcs_vistos = set()

    print(f"A gerar {n} instituições...\n")

    while len(resultados) < n:
        registo = generate_instituicao(localidades)
        nipc    = registo["nif_nipc"]

        if nipc in nipcs_vistos:
            continue

        nipcs_vistos.add(nipc)
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} instituições geradas.\n")
    return resultados