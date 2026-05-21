import random
import unicodedata
from faker import Faker

faker = Faker("pt_PT")

DOMINIOS_EMAIL = ["gmail", "hotmail", "outlook", "sapo", "mail"]

MOTIVOS_SUSPENSAO_CIDADAO = {
    1: "Incumprimento dos termos de utilização",
    2: "Atividade suspeita ou potencial fraude",
    3: "Pedido do próprio cidadão",
    4: "Dados pessoais inválidos ou desatualizados",
}


def _normalizar_email(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    return "".join(c for c in texto.lower() if c.isalnum() or c in ".-_")


def _gerar_contacto(nome: str) -> str:
    partes = nome.strip().split()
    primeiro = _normalizar_email(partes[0] if partes else "cidadao")
    ultimo = _normalizar_email(partes[-1] if len(partes) > 1 else "sam")
    dominio = random.choice(DOMINIOS_EMAIL)
    return f"{primeiro}.{ultimo}@{dominio}.com"[:50]


def generate_cidadao() -> dict:
    blocked = random.choices([0, 1], weights=[50, 50], k=1)[0]
    nome = faker.name()[:50]
    cidadao = {
        "nome": nome,
        "contacto": _gerar_contacto(nome),
        "rgpd": random.choices([0, 1], weights=[10, 90], k=1)[0],
        "blocked": blocked,
        "role": "citizen",
    }

    if blocked == 1:
        cidadao["reason"] = random.choice(
            list(MOTIVOS_SUSPENSAO_CIDADAO.values()))

    return cidadao


def generate_cidadaos(n: int = 100) -> list[dict]:
    resultados = []
    contactos_vistos = set()

    print(f"A gerar {n} cidadãos...\n")

    while len(resultados) < n:
        registo = generate_cidadao()
        contacto = registo["contacto"]

        if contacto in contactos_vistos:
            continue

        contactos_vistos.add(contacto)
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} cidadãos gerados.\n")
    return resultados
