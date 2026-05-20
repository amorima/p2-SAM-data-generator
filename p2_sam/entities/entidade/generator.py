from faker import Faker

faker = Faker("pt_PT")

# Dicionário de nomes falsos de instituições
NOMES_INSTITUICOES = [
    "Casa do Povo", "Lar dos Avós", "Centro de Apoio Social",
    "Fundação Esperança", "Associação Renascer", "Cooperativa Horizonte",
    "Misericórdia do Vale", "União Solidária", "Federação Progresso",
    "IPSS Caridade", "ONG Futuro", "Centro Social Raízes",
    "Fundação Caminho", "Associação Luz", "Cooperativa Fraternidade",
    "Lar São Francisco", "Centro Comunitário Serra", "Associação Rede Viva",
    "Fundação Terra Nova", "União do Bem",
]

# Dicionário de nomes falsos de negócios
NOMES_NEGOCIOS = [
    "TechLuso", "InovaMais", "DigitalPorto", "SolTec", "NovaMed",
    "EcoVerde", "UrbanBuild", "AgroConde", "MarInov", "LogiFlow",
    "DataBridge", "SmartRede", "BioLab", "AquaClean", "GreenEnergy",
    "SafeGuard", "MediCare", "TurboLean", "FlexWork", "NanoTech",
]


def email_pessoa(nome_completo: str) -> str:
    partes = nome_completo.strip().split()
    primeiro = partes[0].lower() if partes else "user"
    ultimo = partes[-1].lower() if len(partes) > 1 else "user"
    dominio = faker.free_email_domain()
    # remove acentos simples para o email
    for a, b in [("ã", "a"), ("á", "a"), ("à", "a"), ("â", "a"), ("é", "e"), ("ê", "e"),
                 ("í", "i"), ("ó", "o"), ("ô", "o"), ("õ", "o"), ("ú", "u"), ("ç", "c")]:
        primeiro = primeiro.replace(a, b)
        ultimo = ultimo.replace(a, b)
    return f"{primeiro}.{ultimo}@{dominio}"[:45]


def email_organizacao(nome: str) -> str:
    slug = nome.lower().replace(" ", "")
    dominio = faker.free_email_domain()
    for a, b in [("ã", "a"), ("á", "a"), ("à", "a"), ("â", "a"), ("é", "e"), ("ê", "e"),
                 ("í", "i"), ("ó", "o"), ("ô", "o"), ("õ", "o"), ("ú", "u"), ("ç", "c")]:
        slug = slug.replace(a, b)
    return f"{slug}@{dominio}"[:45]


def generate_entidades(mecenas: list[dict], negocios: list[dict], instituicoes: list[dict], codigos_postais: list[str] = None) -> list[dict]:
    """
    Agrega todos os NIFs já gerados por mecenas, negocios e instituicoes
    e cria os atributos da tabela Entidade para cada um.
    """
    import random

    resultados = []

    # Mecenas — nome de pessoa, email no formato primeiro.ultimo@dominio
    for mecena in mecenas:
        nome = faker.name()
        resultados.append({
            "nif_nipc": mecena["nif_nipc"],
            "email_login": email_pessoa(nome),
            "password": faker.password(length=12, special_chars=True)[:45],
            "nome_entidade": nome[:100],
            "iban": faker.iban(),
            "codigo_postal": random.choice(codigos_postais) if codigos_postais else None,
            "role": "patron",
        })

    # Negócios — nome do dicionário de negócios
    nomes_neg = NOMES_NEGOCIOS.copy()
    random.shuffle(nomes_neg)
    for i, n in enumerate(negocios):
        nome = nomes_neg[i % len(nomes_neg)] + f" {faker.numerify('##')}"
        resultados.append({
            "nif_nipc": n["nif_nipc"],
            "email_login": email_organizacao(nome),
            "password": faker.password(length=12, special_chars=True)[:45],
            "nome_entidade": nome[:100],
            "iban": faker.iban(),
            "codigo_postal": n.get("_codigo_postal") or (
                random.choice(codigos_postais) if codigos_postais else None
            ),
            "role": "business",
        })

    # Instituições — nome do dicionário de instituições
    nomes_inst = NOMES_INSTITUICOES.copy()
    random.shuffle(nomes_inst)
    for i, inst in enumerate(instituicoes):
        nome = nomes_inst[i % len(nomes_inst)] + f" de {faker.city()}"
        resultados.append({
            "nif_nipc": inst["nif_nipc"],
            "email_login": email_organizacao(nome),
            "password": faker.password(length=12, special_chars=True)[:45],
            "nome_entidade": nome[:100],
            "iban": faker.iban(),
            "codigo_postal": inst.get("codigo_postal") or inst.get("_codigo_postal") or (
                random.choice(codigos_postais) if codigos_postais else None
            ),
            "role": "institution",
        })

    print(f"  Concluído! {len(resultados)} entidades geradas.\n")
    return resultados
