import random
from faker import Faker

faker = Faker("pt_PT")


DESCRICOES_POR_BEM = {
    "Arroz": ("Arroz agulha de 1kg embalado", 1.20, 3.50),
    "Feijão": ("Feijão encarnado e manteiga, embalagens 500g", 1.50, 4.00),
    "Massa": ("Massa esparguete e cotovelos 500g", 1.00, 2.50),
    "Azeite": ("Azeite virgem extra 0,75L", 5.00, 9.00),
    "Açúcar": ("Açúcar branco 1kg refinado", 1.00, 1.80),
    "Sal": ("Sal grosso e fino 1kg", 0.80, 1.50),
    "Leite": ("Leite meio-gordo UHT, pacote 1L", 0.85, 1.60),
    "Conservas de peixe": ("Conservas de atum e sardinha em azeite", 1.50, 3.50),
    "Sopa em pó": ("Sopa instantânea de legumes e galinha", 0.80, 2.00),
    "Farinha": ("Farinha de trigo tipo 65, embalagem 1kg", 0.90, 1.80),
    "Casaco de inverno": ("Casaco quente para adulto, tamanhos S-XL", 25.00, 80.00),
    "Calças de ganga": ("Calças de ganga clássicas, vários tamanhos", 15.00, 45.00),
    "Camisolas": ("Camisolas de algodão, manga comprida", 8.00, 25.00),
    "Meias": ("Pack de 5 pares de meias térmicas", 5.00, 12.00),
    "Roupa interior": ("Roupa interior nova, pacote familiar", 8.00, 20.00),
    "Sapatos": ("Sapatos cómodos para adulto, tamanhos 36-45", 20.00, 60.00),
    "Botas de chuva": ("Botas de borracha impermeáveis", 15.00, 35.00),
    "Fraldas": ("Fraldas descartáveis bebé, tamanhos 1-6", 8.00, 22.00),
    "Champô": ("Champô neutro para cabelos sensíveis 400ml", 2.50, 6.00),
    "Gel de banho": ("Gel de banho hidratante 500ml", 2.00, 5.50),
    "Pasta de dentes": ("Pasta dentífrica com flúor 75ml", 1.50, 4.00),
    "Papel higiénico": ("Papel higiénico 12 rolos, folha dupla", 3.00, 7.00),
    "Pensos higiénicos": ("Pensos higiénicos diários e noturnos", 2.00, 5.00),
    "Sabonete": ("Sabonete neutro hipoalergénico", 1.00, 3.00),
    "Paracetamol": ("Paracetamol 500mg, 20 comprimidos", 1.50, 3.50),
    "Ibuprofeno": ("Ibuprofeno 400mg, 20 comprimidos", 2.50, 5.00),
    "Pensos rápidos": ("Caixa de pensos rápidos sortidos", 2.00, 4.00),
    "Álcool etílico": ("Álcool etílico 96º, 250ml", 1.50, 3.00),
    "Termómetro": ("Termómetro digital de uso doméstico", 5.00, 12.00),
    "Medidor de tensão": ("Medidor de tensão arterial automático", 25.00, 60.00),
    "Vitaminas": ("Multivitamínico polivalente, 30 cápsulas", 6.00, 15.00),
    "Cadernos": ("Cadernos pautados A4, pack de 5", 3.00, 7.00),
    "Lápis e canetas": ("Estojo escolar com lápis, canetas e marcadores", 4.00, 10.00),
    "Mochila escolar": ("Mochila escolar resistente, vários modelos", 15.00, 40.00),
    "Livros escolares": ("Manuais escolares reciclados, 1º-9º ano", 10.00, 35.00),
    "Régua e compasso": ("Kit de geometria escolar", 3.00, 8.00),
    "Borracha": ("Pack de borrachas e afia-lápis", 1.00, 3.00),
    "Passe mensal": ("Passe mensal de transporte público local", 30.00, 45.00),
    "Bilhete de autocarro": ("Caderneta de 10 bilhetes de autocarro", 8.00, 15.00),
    "Bilhete de metro": ("Caderneta de 10 bilhetes de metro", 9.00, 16.00),
    "Cobertor": ("Cobertor polar 1,5x2m", 8.00, 20.00),
    "Lençóis": ("Conjunto de lençóis para cama de solteiro", 12.00, 30.00),
    "Almofada": ("Almofada anti-ácaros, 50x70cm", 5.00, 15.00),
    "Toalhas de banho": ("Toalhas de banho 100% algodão", 6.00, 18.00),
    "Detergente para a roupa": ("Detergente líquido, garrafa 3L", 4.00, 9.00),
    "Lixívia": ("Lixívia tradicional 2L", 1.50, 3.00),
    "Esfregão": ("Pack de esfregões e panos de limpeza", 2.00, 5.00),
    "Brinquedos para crianças": ("Brinquedos didáticos para 3-10 anos", 5.00, 25.00),
    "Material de escritório": ("Material de escritório variado (folhas, agrafos)", 4.00, 12.00),
    "Pilhas": ("Pack de pilhas AA/AAA recarregáveis", 4.00, 10.00),
    "Velas": ("Pack de velas de emergência e tochas", 3.00, 8.00),
    "Lanternas": ("Lanterna LED a pilhas, alta intensidade", 6.00, 15.00),
}

DESCRICOES_POR_SERVICO = {
    "Consulta médica": ("Consultas de medicina geral e familiar", 25.00, 60.00),
    "Consulta de enfermagem": ("Cuidados de enfermagem ao domicílio", 15.00, 35.00),
    "Fisioterapia": ("Sessões de fisioterapia e reabilitação", 20.00, 45.00),
    "Apoio psicológico": ("Acompanhamento psicológico individual e familiar", 30.00, 60.00),
    "Transporte para consultas": ("Transporte para consultas e tratamentos", 8.00, 20.00),
    "Explicações escolares": ("Explicações de Matemática, Português e Inglês", 10.00, 25.00),
    "Aulas de português para imigrantes": ("Aulas de Português Língua Não Materna", 8.00, 20.00),
    "Formação profissional": ("Formação técnica certificada (40h)", 50.00, 150.00),
    "Apoio a literacia digital": ("Sessões de literacia digital para seniores", 6.00, 15.00),
    "Reparações domésticas": ("Pequenas reparações domésticas (canalização, elétrica)", 15.00, 50.00),
    "Limpeza de habitação": ("Serviço de limpeza profissional ao domicílio", 12.00, 30.00),
    "Apoio ao arrendamento": ("Apoio jurídico em contratos de arrendamento", 25.00, 80.00),
    "Pinturas e obras": ("Pinturas interiores e pequenas obras", 20.00, 70.00),
    "Transporte de idosos": ("Transporte adaptado para idosos", 10.00, 25.00),
    "Transporte escolar": ("Transporte escolar para crianças carenciadas", 8.00, 20.00),
    "Serviço de mobilidade reduzida": ("Viaturas adaptadas a mobilidade reduzida", 15.00, 40.00),
    "Apoio jurídico": ("Consultas jurídicas em direito civil e família", 30.00, 90.00),
    "Apoio social": ("Acompanhamento social e atribuição de subsídios", 0.00, 0.00),
    "Acompanhamento de idosos": ("Acompanhamento e companhia a idosos isolados", 8.00, 18.00),
    "Cuidados ao domicílio": ("Cuidados domiciliários personalizados", 12.00, 30.00),
    "Banco de horas voluntário": ("Banco de horas para voluntariado local", 0.00, 0.00),
}


def _descricao_e_valor(tipo_bem_servico: str) -> tuple[str, float]:
    cat = DESCRICOES_POR_BEM.get(tipo_bem_servico) or DESCRICOES_POR_SERVICO.get(tipo_bem_servico)
    if cat is None:
        descricao = f"Oferta de {tipo_bem_servico.lower()} por parte do negócio"
        valor = round(random.uniform(5, 80), 2)
        return descricao, valor
    descricao, val_min, val_max = cat
    if val_min == 0 and val_max == 0:
        valor = 0.00
    else:
        valor = round(random.uniform(val_min, val_max), 2)
    return descricao, valor


def _desconto_realista() -> float:
    """
    Distribuição mais realista de descontos:
    - 30% pro bono (100% de desconto)
    - 25% desconto significativo (50-75%)
    - 25% desconto moderado (25-49%)
    - 20% desconto reduzido (0-24%)
    """
    bucket = random.choices(
        ["pro_bono", "alto", "medio", "baixo"],
        weights=[30, 25, 25, 20],
        k=1,
    )[0]
    if bucket == "pro_bono":
        return 100.00
    if bucket == "alto":
        return round(random.uniform(50, 75), 2)
    if bucket == "medio":
        return round(random.uniform(25, 49), 2)
    return round(random.uniform(0, 24), 2)


def generate_bem_servico_negocio(negocios: list[dict],
                                 bens_servicos: list[dict]) -> dict:
    negocio = random.choice(negocios)
    bem = random.choice(bens_servicos)
    descricao, valor = _descricao_e_valor(bem["tipo_bem_servico"])

    if valor <= 0:
        valor = round(random.uniform(5, 50), 2)

    return {
        "negocio_nif_nipc": negocio["nif_nipc"],
        "tipo_bem_servico": bem["tipo_bem_servico"],
        "descricao": descricao,
        "valor_total": valor,
        "desconto": _desconto_realista(),
    }


def generate_bens_servicos_negocio(n: int = 100, negocios: list[dict] = None,
                                   bens_servicos: list[dict] = None) -> list[dict]:
    if not negocios or not bens_servicos:
        raise ValueError("É necessário fornecer negocios e bens_servicos.")

    max_combinacoes = len(negocios) * len(bens_servicos)
    if n > max_combinacoes:
        raise ValueError(
            f"Não é possível gerar {n} ofertas únicas com "
            f"{len(negocios)} negócios e {len(bens_servicos)} bens/serviços."
        )

    resultados = []
    pares_vistos = set()

    print(f"A gerar {n} bens_serviços_negócio...\n")

    while len(resultados) < n:
        registo = generate_bem_servico_negocio(negocios, bens_servicos)
        par = (registo["negocio_nif_nipc"], registo["tipo_bem_servico"])

        if par in pares_vistos:
            continue

        pares_vistos.add(par)
        resultados.append(registo)

    print(f"  Concluído! {len(resultados)} bens_serviços_negócio gerados.\n")
    return resultados
