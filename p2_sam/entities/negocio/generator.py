import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker("pt_PT")


def _gerar_nipc_negocio() -> str:
    """
    Negócio é uma pessoa coletiva/empresa.
    NIF começa por 5 (coletiva) 1 ou 2 (entidades públicas)
    """
    prefixo = random.choices(["1", "2", "5"], weights=[20, 20, 60], k=1)[0]
    return prefixo + faker.numerify("########")


def _data_inicio_atividade() -> str:
    inicio = datetime.now() - timedelta(days=30 * 365)
    delta = datetime.now() - inicio
    data = inicio + timedelta(days=random.randint(0, delta.days))
    return data.strftime("%Y-%m-%d %H:%M:%S")


def generate_negocio(localidades: list[dict]) -> dict:
    loc = random.choice(localidades)
    nipc = _gerar_nipc_negocio()

    return {
        "nif_nipc": nipc,
        "_codigo_postal": loc["codigo_postal"],
        "geo_latitude": loc["_latitude"],
        "geo_longitude": loc["_longitude"],
        "url_certidao_permanente": f"https://certidoes.negocio.pt/{nipc}.pdf",
        "inicio_atividade": _data_inicio_atividade(),
    }


def generate_negocios(n: int = 50, localidades: list[dict] = None) -> list[dict]:
    if not localidades:
        raise ValueError("É necessário fornecer uma lista de localidades.")

    resultados = []
    nipcs_vistos = set()

    print(f"A gerar {n} negócios...\n")

    while len(resultados) < n:
        registo = generate_negocio(localidades)
        nipc = registo["nif_nipc"]

        if nipc in nipcs_vistos:
            continue

        nipcs_vistos.add(nipc)
        resultados.append(registo)

    # Fixture de teste — NIF fixo para o Postman chain
    if "599999997" not in nipcs_vistos:
        resultados.append({
            "nif_nipc": "599999997",
            "_codigo_postal": localidades[0]["codigo_postal"],
            "geo_latitude": 41.3526,
            "geo_longitude": -8.7396,
            "url_certidao_permanente": "https://certidoes.negocio.pt/599999997.pdf",
            "inicio_atividade": "2020-01-01 00:00:00",
        })

    print(f"  Concluído! {len(resultados)} negócios gerados.\n")
    return resultados
