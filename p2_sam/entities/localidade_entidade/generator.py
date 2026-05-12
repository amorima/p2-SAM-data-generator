def generate_localidade_entidade(entidades: list[dict]) -> list[dict]:
    """
    Cria a tabela de ligação entre Entidade e Localidade.
    Usa o NIF e o código postal já atribuídos em Entidade.
    """
    if not entidades:
        raise ValueError("É necessário fornecer uma lista de entidades.")

    resultados = []

    print("A gerar relações localidade_entidade...\n")

    for entidade in entidades:
        codigo_postal = entidade.get("codigo_postal")

        if not codigo_postal:
            continue

        resultados.append({
            "entidade_nif_nipc": entidade["nif_nipc"],
            "localidade_codigo_postal": codigo_postal,
        })

    print(f"  Concluído! {len(resultados)} relações localidade_entidade geradas.\n")
    return resultados
