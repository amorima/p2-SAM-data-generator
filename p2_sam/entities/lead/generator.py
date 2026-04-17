import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker("pt_PT")

ESTADOS_LEAD = ["ENTREGUE", "PENDENTE", "EXPIRADO"]


def _data_aleatoria(anos_atras: int = 3) -> str:
    inicio = datetime.now() - timedelta(days=anos_atras * 365)
    delta = datetime.now() - inicio
    data = inicio + timedelta(days=random.randint(0, delta.days))
    return data.strftime("%Y-%m-%d %H:%M:%S")


def _gerar_pin() -> str:
    """PIN de entrega alfanumérico de 16 caracteres."""
    return faker.bothify("????####????####")[:16].upper()


def generate_lead(paineis: list[dict], pedidos: list[dict],
                  lockers: list[dict], cidadaos: list[dict]) -> dict:
    painel = random.choice(paineis)
    pedido = random.choice(pedidos)
    locker = random.choice(lockers)
    cidadao = random.choice(cidadaos)

    return {
        "data": _data_aleatoria(),
        "id_painel": painel["id_dispositivo"],
        "nome_cidadao": cidadao["nome"][:50],
        "contacto_cidadao": cidadao["contacto"][:13],
        "id_pedido": pedido["id_pedido"],
        "item_pedido": faker.bothify("ITEM-####-??")[:100],
        "estado": random.choice(ESTADOS_LEAD),
        "pin_entrega": _gerar_pin(),
        "id_locker": locker["id_locker"],
    }


def generate_leads(n: int = 100, paineis: list[dict] = None,
                   pedidos: list[dict] = None, lockers: list[dict] = None,
                   cidadaos: list[dict] = None) -> list[dict]:
    if not all([paineis, pedidos, lockers, cidadaos]):
        raise ValueError(
            "É necessário fornecer paineis, pedidos, lockers e cidadaos.")

    resultados = []

    print(f"A gerar {n} leads...\n")

    for i in range(1, n + 1):
        registo = generate_lead(paineis, pedidos, lockers, cidadaos)
        registo["id_lead"] = i
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} leads gerados.\n")
    return resultados
