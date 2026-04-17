import random
from faker import Faker

faker = Faker("pt_PT")

ESTADOS_LOCKER = ["OCUPADO", "DISPONIVEL", "MANUTENCAO", "INDISPONIVEL"]


def generate_locker(localidades: list[dict]) -> dict:
    """
    Locker Inteligente instalado num local físico
    Coordenadas reais herdadas de uma localidade
    """
    loc = random.choice(localidades)

    return {
        "estado": random.choices(
            ESTADOS_LOCKER,
            weights=[30, 50, 10, 10],
            k=1
        )[0],
        # código alfanumérico de 20 caracteres (? = letra, # = número)
        "codigo_mestre": faker.bothify("??##??##??##??##")[:45],
        "geo_latitude": loc["_latitude"],
        "geo_longitude": loc["_longitude"],
    }


def generate_lockers(n: int = 30, localidades: list[dict] = None) -> list[dict]:
    if not localidades:
        raise ValueError("É necessário fornecer uma lista de localidades.")

    resultados = []

    print(f"A gerar {n} lockers inteligentes...\n")

    for i in range(1, n + 1):
        registo = generate_locker(localidades)
        registo["id_locker"] = i
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} lockers gerados.\n")
    return resultados
