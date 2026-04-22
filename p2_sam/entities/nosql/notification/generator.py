import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker("pt_PT")

TIPOS_NOTIFICACAO = ["EMAIL", "SMS", "PUSH", "SISTEMA"]
ESTADOS_ENVIO = ["ENVIADO", "FALHOU", "PENDENTE", "CANCELADO"]
MOTIVOS_ERRO = [
    "EMAIL_INVALIDO", "SMS_FALHOU", "TIMEOUT", "DESTINATARIO_INEXISTENTE", None, None,
]


def _data_aleatoria(dias_atras: int = 90) -> str:
    inicio = datetime.now() - timedelta(days=dias_atras)
    delta = datetime.now() - inicio
    return (inicio + timedelta(seconds=random.randint(0, int(delta.total_seconds())))).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_notification(leads: list[dict]) -> dict:
    """
    Gera uma notificação associada a uma lead SQL.
    lead_sql_id referencia o id_lead da tabela SQL leads.
    """
    lead = random.choice(leads)
    tipo = random.choice(TIPOS_NOTIFICACAO)
    estado = random.choices(
        ESTADOS_ENVIO,
        weights=[65, 15, 10, 10],
        k=1
    )[0]
    motivo_erro = None if estado == "ENVIADO" else random.choice(
        [m for m in MOTIVOS_ERRO if m])
    tentativas = 1 if estado == "ENVIADO" else random.randint(1, 4)

    if tipo == "EMAIL":
        destinatario = faker.email()
    elif tipo == "SMS":
        prefixo = random.choice(["91", "92", "93", "96"])
        destinatario = prefixo + faker.numerify("#######")
    else:
        destinatario = faker.uuid4()

    return {
        "lead_sql_id": lead["id_lead"],
        "tipo": tipo,
        "destinatario_hash": faker.md5()[:16],
        "data_envio": _data_aleatoria(),
        "estado_envio": estado,
        "tentativas": tentativas,
        "motivo_erro": motivo_erro,
    }


def generate_notifications(n: int = 150, leads: list[dict] = None) -> list[dict]:
    if not leads:
        raise ValueError("É necessário fornecer uma lista de leads.")

    resultados = []

    print(f"A gerar {n} notificações...\n")

    for _ in range(n):
        resultados.append(generate_notification(leads))

    print(f"  Concluído! {len(resultados)} notificações geradas.\n")
    return resultados
