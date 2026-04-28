import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker("pt_PT")

FLUXOS_POSSIVEIS = ["Home", "Mapa", "Ver_Necessidade",
                    "Doar", "Inserir_Contacto", "Confirmar", "Sucesso"]
IDIOMAS = ["pt", "en", "fr", "es"]
PASSOS_ABANDONO = ["Home", "Mapa",
                   "Ver_Necessidade", "Doar", "Inserir_Contacto"]


def _data_aleatoria(dias_atras: int = 90) -> str:
    inicio = datetime.now() - timedelta(days=dias_atras)
    delta = datetime.now() - inicio
    return (inicio + timedelta(seconds=random.randint(0, int(delta.total_seconds())))).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_interaction_log(paineis: list[dict]) -> dict:
    """
    Gera um log de interação de um cidadão num painel digital.
    painel_id referencia o id_dispositivo da tabela SQL painel.
    """
    painel = random.choice(paineis)
    concluiu = random.choices([True, False], weights=[55, 45], k=1)[0]
    duracao = random.randint(10, 120)

    if concluiu:
        fluxo = FLUXOS_POSSIVEIS[:]
    else:
        # abandona num passo aleatório antes do fim
        passo_abandono = random.randint(1, len(PASSOS_ABANDONO))
        fluxo = FLUXOS_POSSIVEIS[:passo_abandono]

    passo_abandono_str = None if concluiu else fluxo[-1]

    return {
        "sessao_id": faker.uuid4(),
        "painel_id": painel["id_dispositivo"],
        "inicio_sessao": _data_aleatoria(),
        "duracao_interacao": duracao,
        "fluxo_navegacao": fluxo,
        "concluiu_doacao": concluiu,
        "passo_abandono": passo_abandono_str,
        "idioma": random.choices(IDIOMAS, weights=[80, 10, 5, 5], k=1)[0],
    }


def generate_interaction_logs(n: int = 300, paineis: list[dict] = None) -> list[dict]:
    if not paineis:
        raise ValueError("É necessário fornecer uma lista de paineis.")

    resultados = []

    print(f"A gerar {n} logs de interação...\n")

    for _ in range(n):
        resultados.append(generate_interaction_log(paineis))

    print(f"  Concluído! {len(resultados)} logs de interação gerados.\n")
    return resultados
