import random
from faker import Faker

faker = Faker("pt_PT")

BENS_POR_CATEGORIA = {
    "alimentação": [
        "arroz", "feijão", "massa", "azeite", "açúcar", "sal",
        "leite", "conservas de peixe", "sopa em pó", "farinha",
    ],
    "vestuário": [
        "casaco de inverno", "calças de ganga", "camisolas",
        "meias", "roupa interior", "sapatos", "botas de chuva",
    ],
    "higiene": [
        "fraldas", "champô", "gel de banho", "pasta de dentes",
        "papel higiénico", "pensos higiénicos", "sabonete",
    ],
    "saúde": [
        "paracetamol", "ibuprofeno", "pensos rápidos", "álcool etílico",
        "termómetro", "medidor de tensão", "vitaminas",
    ],
    "educação": [
        "cadernos", "lápis e canetas", "mochila escolar",
        "livros escolares", "régua e compasso", "borracha",
    ],
    "transporte": [
        "passe mensal", "bilhete de autocarro", "bilhete de metro",
    ],
    "habitação": [
        "cobertor", "lençóis", "almofada", "toalhas de banho",
        "detergente para a roupa", "lixívia", "esfregão",
    ],
    "outro": [
        "brinquedos para crianças", "material de escritório",
        "pilhas", "velas", "lanternas",
    ],
}

SERVICOS_POR_CATEGORIA = {
    "saúde": [
        "consulta médica", "consulta de enfermagem", "fisioterapia",
        "apoio psicológico", "transporte para consultas",
    ],
    "educação": [
        "explicações escolares", "aulas de português para imigrantes",
        "formação profissional", "apoio a literacia digital",
    ],
    "habitação": [
        "reparações domésticas", "limpeza de habitação",
        "apoio ao arrendamento", "pinturas e obras",
    ],
    "transporte": [
        "transporte de idosos", "transporte escolar",
        "serviço de mobilidade reduzida",
    ],
    "outro": [
        "apoio jurídico", "apoio social", "acompanhamento de idosos",
        "cuidados ao domicílio", "banco de horas voluntário",
    ],
}


def generate_bens_servicos() -> list[dict]:
    """
    Gera um registo por cada bem e serviço dos dicionários.
    tipo_bem_servico é a PK — cada entrada é única e estática.
    tipo_bem mapeia para o ENUM do model: 'bem' ou 'servico'.
    """
    resultados = []

    for categoria, bens in BENS_POR_CATEGORIA.items():
        for bem in bens:
            resultados.append({
                "tipo_bem_servico": bem,
                "tipo_bem": "bem",
            })

    for categoria, servicos in SERVICOS_POR_CATEGORIA.items():
        for servico in servicos:
            resultados.append({
                "tipo_bem_servico": servico,
                "tipo_bem": "servico",
            })

    print(f"  Concluído! {len(resultados)} bens e serviços gerados.\n")
    return resultados
