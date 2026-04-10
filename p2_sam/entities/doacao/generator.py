import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker("pt_PT")

# Tipos de donativo conforme diagrama (ENUM)
TIPOS_DONATIVO = ["monetario", "especie", "servico", "voluntariado"]

# Estados da doação (ENUM)
ESTADOS_DOACAO = ["pendente", "confirmado", "cancelado"]


def _gerar_nif_mecena() -> str:
    """
    Gera um NIF/NIPC para Mecena.
    Distribuição realista:
        1 , 2 → pessoa singular 
        5  → pessoas coletivas
        9  → pessoas coletivas ou sociedade irregular para ser mais próximo da realidade

    O Mecena é tipicamente uma empresa ou organização, daí 9 ser dominante e 5.
    """
    prefixo = random.choices(
        ["1", "2", "5", "9"],
        weights=[10, 5, 25, 60], # aplicar peso ao prefixo de cada nif 
        k=1
    )[0]
    return prefixo + faker.numerify("########")


def generate_mecena() -> dict:
    """
    Gera um registo de Mecena.
    Mecena herda de Entidade (nif_nipc é a PK partilhada).
    """
    return {
        "nif_nipc" : _gerar_nif_mecena(),
    }


def generate_mecenas(n: int = 50) -> list[dict]:
    """Gera n mecenas únicos (por nif_nipc)."""
    resultados  = []
    nifs_vistos = set()

    print(f"A gerar {n} mecenas...\n")

    while len(resultados) < n:
        registo = generate_mecena()
        nif     = registo["nif_nipc"]

        if nif in nifs_vistos:
            continue

        nifs_vistos.add(nif)
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} mecenas gerados.\n")
    return resultados


def _data_aleatoria(anos_atras: int = 5) -> str:
    """Gera uma data aleatória nos últimos n anos."""
    inicio = datetime.now() - timedelta(days=anos_atras * 365)
    delta  = datetime.now() - inicio
    data   = inicio + timedelta(days=random.randint(0, delta.days))
    return data.strftime("%Y-%m-%d %H:%M:%S")


def generate_doacao(mecenas: list[dict]) -> dict:
    """
    Gera um registo de Doação ligado a um Mecena existente
    """
    mecena   = random.choice(mecenas)
    anonimo  = random.choices([0, 1], weights=[75, 25], k=1)[0]
    tipo     = random.choice(TIPOS_DONATIVO)
    valor    = round(random.uniform(50, 50000), 2)
    nif      = mecena["nif_nipc"]

    return {
        "mecena_nif_nipc"  : nif,
        "data"             : _data_aleatoria(anos_atras=5),
        "valor_transacao"  : valor,
        "tipo_donativo"    : tipo,
        "anonimo"          : anonimo,
        "url_comprovativo" : f"https://comprovativos.mecenas.pt/{nif}-{faker.numerify('######')}.pdf",
        "estado"           : random.choice(ESTADOS_DOACAO),
    }


def generate_doacoes(n: int = 200, mecenas: list[dict] = None) -> list[dict]:
    """
    Gera n doações ligadas a mecenas existentes
    Uma doação não precisa de ser única — o mesmo mecena pode doar várias vezes
    """
    if not mecenas:
        raise ValueError("É necessário fornecer uma lista de mecenas.")

    resultados = []

    print(f"A gerar {n} doações...\n")

    for i in range(1, n + 1):
        registo = generate_doacao(mecenas)
        registo["id_doacao"] = i
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} doações geradas.\n")
    return resultados