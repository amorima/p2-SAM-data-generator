import random
from faker import Faker

faker = Faker("pt_PT")


# Pedido_Bens_E_Servicos

def generate_pedido_bem_servico(pedidos: list[dict], bens_servicos: list[dict]) -> dict:
    pedido = random.choice(pedidos)
    bem = random.choice(bens_servicos)

    return {
        "id_pedido": pedido["id_pedido"],
        "tipo_bem_servico": bem["tipo_bem_servico"],
        "publico": random.choices([0, 1], weights=[30, 70], k=1)[0],
    }


def generate_pedidos_bens_servicos(n: int = 150, pedidos: list[dict] = None, bens_servicos: list[dict] = None) -> list[dict]:
    if not pedidos or not bens_servicos:
        raise ValueError("É necessário fornecer pedidos e bens_servicos.")

    # Painel só aceita bens físicos para doação — exclui serviços
    apenas_bens = [b for b in bens_servicos if b.get("tipo_bem") == "bem"]
    if not apenas_bens:
        raise ValueError("Não existem bens (tipo_bem='bem') para gerar pedidos.")

    resultados = []
    pares_vistos = set()

    print(f"A gerar {n} pedido_bens_serviços...\n")

    while len(resultados) < n:
        registo = generate_pedido_bem_servico(pedidos, apenas_bens)
        par = (registo["id_pedido"], registo["tipo_bem_servico"])

        if par in pares_vistos:
            continue

        pares_vistos.add(par)
        resultados.append(registo)

    # Fixture de teste — item ZZZ_Teste_Chain para o pedido fixture (599999998)
    fixture_pedido = next((p for p in pedidos if p.get("nif_nipc") == "599999998"), None)
    if fixture_pedido:
        par = (fixture_pedido["id_pedido"], "ZZZ_Teste_Chain")
        if par not in pares_vistos:
            resultados.append({
                "id_pedido": fixture_pedido["id_pedido"],
                "tipo_bem_servico": "ZZZ_Teste_Chain",
                "publico": 1,
            })

    print(f"  Concluído! {len(resultados)} pedido_bens_serviços gerados.\n")
    return resultados


# Bens_E_Servicos_Negocio

def generate_bem_servico_negocio(negocios: list[dict],
                                 bens_servicos: list[dict]) -> dict:
    negocio = random.choice(negocios)
    bem = random.choice(bens_servicos)

    return {
        "negocio_nif_nipc": negocio["nif_nipc"],
        "tipo_bem_servico": bem["tipo_bem_servico"],
        "descricao": faker.sentence(nb_words=10)[:255],
        "valor_total": round(random.uniform(5, 5000), 2),
        "desconto": round(random.uniform(0, 50), 2),
    }


def generate_bens_servicos_negocio(n: int = 100, negocios: list[dict] = None, bens_servicos: list[dict] = None) -> list[dict]:
    if not negocios or not bens_servicos:
        raise ValueError("É necessário fornecer negocios e bens_servicos.")

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
