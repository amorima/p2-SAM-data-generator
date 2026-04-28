import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker("pt_PT")

ESTADOS_VOUCHER = ["ATIVO", "USADO", "EXPIRADO", "CANCELADO"]


def _data_aleatoria(dias_atras: int = 180) -> str:
    inicio = datetime.now() - timedelta(days=dias_atras)
    delta = datetime.now() - inicio
    return (inicio + timedelta(seconds=random.randint(0, int(delta.total_seconds())))).strftime("%Y-%m-%dT%H:%M:%SZ")


def _data_validade(dias_frente: int = 365) -> str:
    return (datetime.now() + timedelta(days=random.randint(30, dias_frente))).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_voucher(entidades: list[dict], negocios: list[dict]) -> dict:
    """
    Gera um voucher associado a uma entidade beneficiária e a um negócio parceiro.
    entidades_disp referencia nif_nipc da tabela SQL entidade.
    """
    estado = random.choices(
        ESTADOS_VOUCHER,
        weights=[50, 25, 15, 10],
        k=1
    )[0]

    entidade = random.choice(entidades)
    negocio = random.choice(negocios)
    montante = round(random.uniform(10, 500), 2)
    data_emissao = _data_aleatoria()
    data_uso = _data_aleatoria(dias_atras=30) if estado == "USADO" else None

    return {
        "montante": str(montante),
        "data_emissao": data_emissao,
        "estado": estado,
        "validade": _data_validade(),
        "entidades_disp": entidade["nif_nipc"],
        "negocio_nif_nipc": negocio["nif_nipc"],
        "data_uso": data_uso,
    }


def generate_vouchers(n: int = 100, entidades: list[dict] = None,
                      negocios: list[dict] = None) -> list[dict]:
    if not entidades or not negocios:
        raise ValueError("É necessário fornecer entidades e negocios.")

    resultados = []

    print(f"A gerar {n} vouchers...\n")

    for _ in range(n):
        resultados.append(generate_voucher(entidades, negocios))

    print(f"  Concluído! {len(resultados)} vouchers gerados.\n")
    return resultados
