import random
from faker import Faker
from p2_sam.utils.dates import data_organica

faker = Faker("pt_PT")

ESTADOS_PEDIDO = ["PENDENTE", "REJEITADO", "ACEITE"]


def generate_pedido(instituicoes: list[dict]) -> dict:
    instituicao = random.choice(instituicoes)

    return {
        "nif_nipc" : instituicao["nif_nipc"],
        "estado"   : random.choices(
                        ESTADOS_PEDIDO,
                        weights=[40, 10, 50], # mais pedidos aceites
                        k=1
                     )[0],
        "data"     : data_organica(),
    }


def generate_pedidos(n: int = 100, instituicoes: list[dict] = None) -> list[dict]:
    if not instituicoes:
        raise ValueError("É necessário fornecer uma lista de instituicoes.")

    resultados = []

    print(f"A gerar {n} pedidos...\n")

    for i in range(1, n + 1):
        registo = generate_pedido(instituicoes)
        registo["id_pedido"] = i
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} pedidos gerados.\n")
    return resultados