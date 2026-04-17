import random
from faker import Faker

faker = Faker("pt_PT")

TIPOS_CONTACTO = ["email", "telefone", "telemovel", "fax", "outro"]


def _gerar_valor_contacto(tipo: str) -> str:
    if tipo == "email":
        return faker.email()[:45]
    elif tipo in ("telefone", "fax"):
        return faker.numerify("2########")[:45]
    elif tipo == "telemovel":
        prefixo = random.choice(["91", "92", "93", "96"])
        return (prefixo + faker.numerify("#######"))[:45]
    else:
        return faker.bothify("??-########")[:45]


def generate_contactos(entidades: list[dict], contactos_por_entidade: int = 1) -> list[dict]:
    """
    Para cada entidade gerada, cria contactos_por_entidade contactos.
    O nif_nipc é herdado diretamente da entidade — não são gerados NIFs novos.
    """
    resultados = []
    contactos_vistos = set()

    print(f"A gerar contactos para {len(entidades)} entidades...\n")

    for entidade in entidades:
        criados = 0
        tentativas = 0

        while criados < contactos_por_entidade:
            tentativas += 1
            if tentativas > 50:
                break  # evita loop infinito se tipos se esgotarem

            tipo = random.choice(TIPOS_CONTACTO)
            contacto = _gerar_valor_contacto(tipo)

            if contacto in contactos_vistos:
                continue

            contactos_vistos.add(contacto)
            resultados.append({
                "contacto": contacto,
                "entidade_nif_nipc": entidade["nif_nipc"],
                "nome_contacto": entidade["nome_entidade"][:100],
                "descricao": faker.sentence(nb_words=8)[:500],
            })
            criados += 1

    print(f"  Concluído! {len(resultados)} contactos gerados.\n")
    return resultados
