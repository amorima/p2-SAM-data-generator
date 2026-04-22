import random
from faker import Faker

faker = Faker("pt_PT")

BENS_POR_CATEGORIA = {
    "alimentacao": [
        "Arroz", "Feijão", "Massa", "Azeite", "Açúcar", "Sal",
        "Leite", "Conservas de peixe", "Sopa em pó", "Farinha",
    ],
    "vestuario": [
        "Casaco de inverno", "Calças de ganga", "Camisolas",
        "Meias", "Roupa interior", "Sapatos", "Botas de chuva",
    ],
    "higiene": [
        "Fraldas", "Champô", "Gel de banho", "Pasta de dentes",
        "Papel higiénico", "Pensos higiénicos", "Sabonete",
    ],
    "saude": [
        "Paracetamol", "Ibuprofeno", "Pensos rápidos", "Álcool etílico",
        "Termómetro", "Medidor de tensão", "Vitaminas",
    ],
    "educacao": [
        "Cadernos", "Lápis e canetas", "Mochila escolar",
        "Livros escolares", "Régua e compasso", "Borracha",
    ],
    "transporte": [
        "Passe mensal", "Bilhete de autocarro", "Bilhete de metro",
    ],
    "habitacao": [
        "Cobertor", "Lençóis", "Almofada", "Toalhas de banho",
        "Detergente para a roupa", "Lixívia", "Esfregão",
    ],
    "outro": [
        "Brinquedos para crianças", "Material de escritório",
        "Pilhas", "Velas", "Lanternas",
    ],
}


def generate_bens_servicos() -> list[dict]:
    """
    Gera um registo por cada bem do dicionário, associado à sua categoria.
    tipo_bem_servico é a PK — cada bem é único e estático.
    tipo mapeia para o ENUM do model: 'bem' ou 'servico'.
    """
    resultados = []

    for categoria, bens in BENS_POR_CATEGORIA.items():
        for bem in bens:
            resultados.append({
                "tipo_bem_servico": bem,
                "tipo_bem": "bem",
            })

    print(f"  Concluído! {len(resultados)} bens e serviços gerados.\n")
    return resultados
