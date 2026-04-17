import random
from faker import Faker

faker = Faker("pt_PT")


def _gerar_contacto() -> str:
    """Número de telemóvel português: 9X com 9 dígitos."""
    prefixo = random.choice(["91", "92", "93", "96"])
    return prefixo + faker.numerify("#######")


def generate_cidadao() -> dict:
    return {
        "nome"     : faker.name()[:50],
        "contacto" : _gerar_contacto(),
        "rgpd"     : random.choices([0, 1], weights=[10, 90], k=1)[0],
    }


def generate_cidadaos(n: int = 100) -> list[dict]:
    resultados      = []
    contactos_vistos = set()

    print(f"A gerar {n} cidadãos...\n")

    while len(resultados) < n:
        registo   = generate_cidadao()
        contacto  = registo["contacto"]

        if contacto in contactos_vistos:
            continue

        contactos_vistos.add(contacto)
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} cidadãos gerados.\n")
    return resultados