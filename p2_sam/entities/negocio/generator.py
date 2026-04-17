import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker("pt_PT")


def _gerar_nipc_negocio() -> str:
    """
    Negócio é uma pessoa coletiva/empresa.
    NIF começa por 5 (entidade pública) ou 9 (empresa privada).
    Maioria começa por 9.
    """
    prefixo = random.choices(["5", "9"], weights=[20, 80], k=1)[0]
    return prefixo + faker.numerify("########")


def _data_inicio_atividade() -> str:
    inicio = datetime.now() - timedelta(days=30 * 365)
    delta  = datetime.now() - inicio
    data   = inicio + timedelta(days=random.randint(0, delta.days))
    return data.strftime("%Y-%m-%d %H:%M:%S")


def generate_negocio(localidades: list[dict]) -> dict:
    loc  = random.choice(localidades)
    nipc = _gerar_nipc_negocio()

    return {
        "nif_nipc"              : nipc,
        "geo_latitude"          : loc["_latitude"],
        "geo_longitude"         : loc["_longitude"],
        "url_certidao_permanente": f"https://certidoes.negocio.pt/{nipc}.pdf",
        "inicio_atividade"      : _data_inicio_atividade(),
    }


def generate_negocios(n: int = 50, localidades: list[dict] = None) -> list[dict]:
    if not localidades:
        raise ValueError("É necessário fornecer uma lista de localidades.")

    resultados   = []
    nipcs_vistos = set()

    print(f"A gerar {n} negócios...\n")

    while len(resultados) < n:
        registo = generate_negocio(localidades)
        nipc    = registo["nif_nipc"]

        if nipc in nipcs_vistos:
            continue

        nipcs_vistos.add(nipc)
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} negócios gerados.\n")
    return resultados