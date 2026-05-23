import random
from faker import Faker
from p2_sam.utils.dates import data_organica

faker = Faker("pt_PT")

ESTADOS_LEAD = ["ENTREGUE", "PENDENTE", "EXPIRADO"]


def generate_lead(paineis: list[dict], pedidos_bens: list[dict],
                  lockers: list[dict], cidadaos: list[dict]) -> dict:
    painel = random.choice(paineis)
    pedido_bem = random.choice(pedidos_bens)
    locker = random.choice(lockers)
    cidadao = random.choice(cidadaos)

    return {
        "data": data_organica(),
        "id_painel": painel["id_dispositivo"],
        "nome_cidadao": cidadao["nome"][:50],
        "contacto_cidadao": cidadao["contacto"][:50],
        "id_pedido": pedido_bem["id_pedido"],
        "item_pedido": pedido_bem["tipo_bem_servico"][:100],
        "estado": random.choice(ESTADOS_LEAD),
        "pin_entrega": faker.numerify("######"),
        "id_locker": locker["id_locker"],
    }


def generate_leads(n: int = 100, paineis: list[dict] = None,
                   pedidos_bens: list[dict] = None, lockers: list[dict] = None,
                   cidadaos: list[dict] = None,
                   bens_servicos: list[dict] = None) -> list[dict]:
    if not all([paineis, pedidos_bens, lockers, cidadaos]):
        raise ValueError(
            "É necessário fornecer paineis, pedidos_bens, lockers e cidadaos.")

    if bens_servicos is not None:
        tipos_bem = {
            item["tipo_bem_servico"]
            for item in bens_servicos
            if item["tipo_bem"] == "bem"
        }
        pedidos_bens = [
            pedido_bem for pedido_bem in pedidos_bens
            if pedido_bem["tipo_bem_servico"] in tipos_bem
        ]

    if not pedidos_bens:
        raise ValueError("Não existem pedidos de bens para gerar leads.")

    resultados = []

    print(f"A gerar {n} leads...\n")

    for i in range(1, n + 1):
        registo = generate_lead(paineis, pedidos_bens, lockers, cidadaos)
        registo["id_lead"] = i
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} leads gerados.\n")
    return resultados
