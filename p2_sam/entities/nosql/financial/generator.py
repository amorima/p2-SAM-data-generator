import random
from faker import Faker

faker = Faker("pt_PT")

METODOS = ["MBWAY", "MULTIBANCO", "TRANSFERENCIA", "CHEQUE", "NUMERARIO"]
GATEWAYS = ["SIBS", "IFTHENPAY", "EASYPAY", "EUPAGO"]
ESTADOS_GATEWAY = ["SUCESSO", "FALHA", "TIMEOUT", "RECUSADO"]
MOTIVOS_ERRO = ["SALDO_INSUFICIENTE", "CARTAO_EXPIRADO",
                "TIMEOUT_GATEWAY", "RECUSADO_BANCO", "DADOS_INVALIDOS",]


def generate_financial_logs(doacoes: list[dict] = None) -> list[dict]:
    """
    Gera um log financeiro por cada doação existente.
    Garante cobertura total — todas as doações têm registo de auditoria.
    transacao_sql_id referencia o id_doacao da tabela SQL doacao.
    A data do log é a mesma da doação para consistência.
    """
    if not doacoes:
        raise ValueError("É necessário fornecer uma lista de doações.")

    resultados = []

    print(f"A gerar {len(doacoes)} logs financeiros...\n")

    for doacao in doacoes:
        metodo = random.choice(METODOS)
        gateway = random.choice(GATEWAYS)
        estado = random.choices(
            ESTADOS_GATEWAY,
            weights=[70, 15, 10, 5],
            k=1
        )[0]
        erro = None if estado == "SUCESSO" else random.choice(MOTIVOS_ERRO)

        gateway_response = {
            "gateway": gateway,
            "codigo_aprovacao": faker.bothify("##") if estado == "SUCESSO" else None,
            "id_pedido_sibs": faker.bothify("????-####") if metodo in ("MBWAY", "MULTIBANCO") else None,
        }

        if metodo == "MBWAY":
            gateway_response["telemovel_hash"] = faker.md5()[:12]
        elif metodo == "MULTIBANCO":
            gateway_response["referencia"] = faker.numerify("#########")

        resultados.append({
            "transacao_sql_id": doacao["id_doacao"],
            "metodo": metodo,
            "data": doacao["data"],
            "gateway": gateway,
            "telemovel_hash": faker.md5()[:12] if metodo == "MBWAY" else None,
            "codigo_aprovacao": gateway_response["codigo_aprovacao"],
            "id_pedido_sibs": gateway_response.get("id_pedido_sibs"),
            "ip_dispositivo": faker.ipv4(),
            "tentativas": random.randint(1, 3),
            "motivo_erro": erro,
            "status_gateway": estado,
            "gateway_response": gateway_response,
        })

    print(f"  Concluído! {len(resultados)} logs financeiros gerados.\n")
    return resultados
