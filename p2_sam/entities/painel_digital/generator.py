import random
from faker import Faker

faker = Faker("pt_PT")


def generate_painel(localidades: list[dict]) -> dict:
    """
    Painel Digital (dispositivo físico instalado num local).
    Coordenadas reais herdadas de uma localidade.
    """
    loc = random.choice(localidades)

    return {
        "token_api"     : faker.uuid4(),
        "geo_latitude"  : loc["_latitude"],
        "geo_longitude" : loc["_longitude"],
        "raio_alcance"  : random.randint(50, 500),
    }


def generate_paineis(n: int = 30, localidades: list[dict] = None) -> list[dict]:
    if not localidades:
        raise ValueError("É necessário fornecer uma lista de localidades.")

    resultados = []

    print(f"A gerar {n} painéis digitais...\n")

    for i in range(1, n + 1):
        registo = generate_painel(localidades)
        registo["id_dispositivo"] = i
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} painéis gerados.\n")
    return resultados