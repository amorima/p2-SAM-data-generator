import random
from faker import Faker

faker = Faker("pt_PT")

TIPOS_BENS_SERVICOS = ["alimentacao", "vestuario", "higiene",
                       "saude", "educacao", "transporte", "habitacao", "outro"]


def _generate_bem_servico() -> dict:
    tipo_bem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quis bibendum leo, a malesuada erat"

    return {
        "tipo_bem_servico": tipo_bem,
        "tipo": random.choice(TIPOS_BENS_SERVICOS),
    }


def generate_bens_servicos(n: int = 50) -> list[dict]:
    resultados = []
    tipos_vistos = set()

    print(f"A gerar {n} bens e serviços...\n")

    while len(resultados) < n:
        registo = _generate_bem_servico()
        tipo = registo["tipo_bem_servico"]

        if tipo in tipos_vistos:
            continue

        tipos_vistos.add(tipo)
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} bens e serviços gerados.\n")
    return resultados
