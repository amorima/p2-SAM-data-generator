import random
from faker import Faker

faker = Faker("pt_PT")

BENS_POR_CATEGORIA = {
    "alimentacao": [
        "arroz", "feijao", "massa", "azeite", "acucar", "sal",
        "leite", "conservas de peixe", "sopa em po", "farinha",
    ],
    "vestuario": [
        "casaco de inverno", "calcas de ganga", "camisolas",
        "meias", "roupa interior", "sapatos", "botas de chuva",
    ],
    "higiene": [
        "fraldas", "champo", "gel de banho", "pasta de dentes",
        "papel higienico", "pensos higienicos", "sabonete",
    ],
    "saude": [
        "paracetamol", "ibuprofeno", "pensos rapidos", "alcool etilico",
        "termometro", "medidor de tensao", "vitaminas",
    ],
    "educacao": [
        "cadernos", "lapis e canetas", "mochila escolar",
        "livros escolares", "regua e compasso", "borracha",
    ],
    "transporte": [
        "passe mensal", "bilhete de autocarro", "bilhete de metro",
    ],
    "habitacao": [
        "cobertor", "lencois", "almofada", "toalhas de banho",
        "detergente para a roupa", "lixivia", "esfregao",
    ],
    "outro": [
        "brinquedos para criancas", "material de escritorio",
        "pilhas", "velas", "lanternas",
    ],
}

SERVICOS_POR_CATEGORIA = {
    "saude": [
        "consulta medica", "consulta de enfermagem", "fisioterapia",
        "apoio psicologico", "transporte para consultas",
    ],
    "educacao": [
        "explicacoes escolares", "aulas de portugues para imigrantes",
        "formacao profissional", "apoio a literacia digital",
    ],
    "habitacao": [
        "reparacoes domesticas", "limpeza de habitacao",
        "apoio ao arrendamento", "pinturas e obras",
    ],
    "transporte": [
        "transporte de idosos", "transporte escolar",
        "servico de mobilidade reduzida",
    ],
    "outro": [
        "apoio juridico", "apoio social", "acompanhamento de idosos",
        "cuidados ao domicilio", "banco de horas voluntario",
    ],
}


def generate_bens_servicos() -> list[dict]:
    """
    Gera um registo por cada bem e serviço dos dicionários.
    tipo_bem_servico é a PK — cada entrada é única e estática.
    tipo mapeia para o ENUM do model: 'bem' ou 'servico'.
    """
    resultados = []

    for categoria, bens in BENS_POR_CATEGORIA.items():
        for bem in bens:
            resultados.append({
                "tipo_bem_servico": bem,
                "tipo": "bem",
            })

    for categoria, servicos in SERVICOS_POR_CATEGORIA.items():
        for servico in servicos:
            resultados.append({
                "tipo_bem_servico": servico,
                "tipo": "servico",
            })

    print(f"  Concluído! {len(resultados)} bens e serviços gerados.\n")
    return resultados
