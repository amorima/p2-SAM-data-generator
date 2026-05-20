import random
from faker import Faker

faker = Faker("pt_PT")


def generate_bem_servico_negocio(negocios: list[dict],
                                 bens_servicos: list[dict]) -> dict:
    negocio = random.choice(negocios)
    bem = random.choice(bens_servicos)

    return {
        "negocio_nif_nipc": negocio["nif_nipc"],
        "tipo_bem_servico": bem["tipo_bem_servico"],
        "descricao": "Lorem Ipsum neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit",
        "valor_total": round(random.uniform(5, 5000), 2),
        "desconto": round(random.uniform(0, 50), 2),
    }


def generate_bens_servicos_negocio(n: int = 100, negocios: list[dict] = None,
                                   bens_servicos: list[dict] = None) -> list[dict]:
    if not negocios or not bens_servicos:
        raise ValueError("É necessário fornecer negocios e bens_servicos.")

    max_combinacoes = len(negocios) * len(bens_servicos)
    if n > max_combinacoes:
        raise ValueError(
            f"Não é possível gerar {n} ofertas únicas com "
            f"{len(negocios)} negócios e {len(bens_servicos)} bens/serviços."
        )

    resultados = []
    pares_vistos = set()

    print(f"A gerar {n} bens_serviços_negócio...\n")

    while len(resultados) < n:
        registo = generate_bem_servico_negocio(negocios, bens_servicos)
        par = (registo["negocio_nif_nipc"], registo["tipo_bem_servico"])

        if par in pares_vistos:
            continue

        pares_vistos.add(par)
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} bens_serviços_negócio gerados.\n")
    return resultados
