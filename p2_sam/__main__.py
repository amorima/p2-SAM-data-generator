from pathlib import Path

from p2_sam.entities.localidade.generator import generate_localidades, strip_internal_fields
from p2_sam.entities.doacao.generator import generate_mecenas
from p2_sam.entities.negocio.generator import generate_negocios
from p2_sam.entities.instituicao.generator import generate_instituicoes
from p2_sam.entities.entidade.generator import generate_entidades
from p2_sam.entities.localidade_entidade.generator import generate_localidade_entidade
from p2_sam.entities.contacto.generator import generate_contactos
from p2_sam.entities.doacao.generator import generate_doacoes
from p2_sam.entities.painel_digital.generator import generate_paineis
from p2_sam.entities.locker.generator import generate_lockers
from p2_sam.entities.cidadao.generator import generate_cidadaos
from p2_sam.entities.pedido.generator import generate_pedidos
from p2_sam.entities.bens_servicos.generator import generate_bens_servicos
from p2_sam.entities.pedido_bens_servico.generator import generate_pedidos_bens_servicos
from p2_sam.entities.bens_e_servicos_negocio.generator import generate_bens_servicos_negocio
from p2_sam.entities.lead.generator import generate_leads
from p2_sam.exporters.csv_exporter import export_csv
from p2_sam.exporters.json_exporter import export_json
from p2_sam.entities.nosql.locker_telemetry.generator import generate_locker_telemetries
from p2_sam.entities.nosql.financial.generator import generate_financial_logs
from p2_sam.entities.nosql.interaction.generator import generate_interaction_logs
from p2_sam.entities.nosql.notification.generator import generate_notifications
from p2_sam.entities.nosql.voucher.generator import generate_vouchers
from p2_sam.exporters.mongodb_exporter import export_nosql


OUTPUT_DIR = Path(__file__).parent.parent / "output"
TOTAL_ETAPAS = 21


def _mostrar_etapa(numero: int, total: int, descricao: str) -> None:
    print(f"\n[{numero}/{total}] A gerar {descricao}...", flush=True)


def main() -> None:
    print("\nA iniciar geracao de dados sinteticos do SAM...", flush=True)
    print("Este processo pode demorar alguns segundos.\n", flush=True)

    # 1 — Localidade (base para coordenadas)
    _mostrar_etapa(1, TOTAL_ETAPAS, "localidades")
    localidades = generate_localidades(n=100)
    codigos_postais = [loc["codigo_postal"] for loc in localidades]
    export_csv(strip_internal_fields(localidades),  "localidade", OUTPUT_DIR)
    export_json(strip_internal_fields(localidades), "localidade", OUTPUT_DIR)

    # 2 — Entidades próprias (geram os seus NIFs)
    _mostrar_etapa(2, TOTAL_ETAPAS, "mecenas")
    mecenas = generate_mecenas(n=50)
    export_csv(mecenas,  "mecena", OUTPUT_DIR)
    export_json(mecenas, "mecena", OUTPUT_DIR)

    _mostrar_etapa(3, TOTAL_ETAPAS, "negocios")
    negocios = generate_negocios(n=50, localidades=localidades)
    export_csv(strip_internal_fields(negocios),  "negocio", OUTPUT_DIR)
    export_json(strip_internal_fields(negocios), "negocio", OUTPUT_DIR)

    _mostrar_etapa(4, TOTAL_ETAPAS, "instituicoes")
    instituicoes = generate_instituicoes(n=50, localidades=localidades)
    export_csv(instituicoes,  "instituicao", OUTPUT_DIR)
    export_json(instituicoes, "instituicao", OUTPUT_DIR)

    # 3 — Entidade agrega NIFs já gerados e cria email/password/iban
    _mostrar_etapa(5, TOTAL_ETAPAS, "entidades")
    entidades = generate_entidades(
        mecenas=mecenas,
        negocios=negocios,
        instituicoes=instituicoes,
        codigos_postais=codigos_postais,
    )
    export_csv(entidades,  "entidade", OUTPUT_DIR)
    export_json(entidades, "entidade", OUTPUT_DIR)

    _mostrar_etapa(6, TOTAL_ETAPAS, "relacoes localidade_entidade")
    localidade_entidade = generate_localidade_entidade(entidades=entidades)
    export_csv(localidade_entidade,  "localidade_entidade", OUTPUT_DIR)
    export_json(localidade_entidade, "localidade_entidade", OUTPUT_DIR)

    # 4 — Contacto herda NIFs de entidade
    _mostrar_etapa(7, TOTAL_ETAPAS, "contactos")
    contactos = generate_contactos(
        entidades=entidades, contactos_por_entidade=1)
    export_csv(contactos,  "contacto", OUTPUT_DIR)
    export_json(contactos, "contacto", OUTPUT_DIR)

    # 5 — Dependem de mecenas
    _mostrar_etapa(8, TOTAL_ETAPAS, "doacoes")
    doacoes = generate_doacoes(n=200, mecenas=mecenas)
    export_csv(doacoes,  "doacao", OUTPUT_DIR)
    export_json(doacoes, "doacao", OUTPUT_DIR)

    # 6 — Dispositivos físicos (dependem de localidades)
    _mostrar_etapa(9, TOTAL_ETAPAS, "paineis digitais")
    paineis = generate_paineis(n=30, localidades=localidades)
    export_csv(paineis,  "painel_digital", OUTPUT_DIR)
    export_json(paineis, "painel_digital", OUTPUT_DIR)

    _mostrar_etapa(10, TOTAL_ETAPAS, "lockers inteligentes")
    lockers = generate_lockers(n=30, localidades=localidades)
    export_csv(lockers,  "locker", OUTPUT_DIR)
    export_json(lockers, "locker", OUTPUT_DIR)

    # 7 — Sem dependências externas
    _mostrar_etapa(11, TOTAL_ETAPAS, "cidadaos")
    cidadaos = generate_cidadaos(n=100)
    export_csv(cidadaos,  "cidadao", OUTPUT_DIR)
    export_json(cidadaos, "cidadao", OUTPUT_DIR)

    _mostrar_etapa(12, TOTAL_ETAPAS, "bens e servicos")
    bens_servicos = generate_bens_servicos()
    export_csv(bens_servicos,  "bens_servicos", OUTPUT_DIR)
    export_json(bens_servicos, "bens_servicos", OUTPUT_DIR)

    # 8 — Pedidos (dependem de entidades)
    _mostrar_etapa(13, TOTAL_ETAPAS, "pedidos")
    pedidos = generate_pedidos(n=100, instituicoes=instituicoes)
    export_csv(pedidos,  "pedido", OUTPUT_DIR)
    export_json(pedidos, "pedido", OUTPUT_DIR)

    # 9 — Tabelas de relação
    _mostrar_etapa(14, TOTAL_ETAPAS, "pedido_bens_servicos")
    pedidos_bens = generate_pedidos_bens_servicos(
        n=150, pedidos=pedidos, bens_servicos=bens_servicos
    )
    export_csv(pedidos_bens,  "pedido_bens_servicos", OUTPUT_DIR)
    export_json(pedidos_bens, "pedido_bens_servicos", OUTPUT_DIR)

    _mostrar_etapa(15, TOTAL_ETAPAS, "bens_servicos_negocio")
    bens_negocio = generate_bens_servicos_negocio(
        n=100, negocios=negocios, bens_servicos=bens_servicos
    )
    export_csv(bens_negocio,  "bens_servicos_negocio", OUTPUT_DIR)
    export_json(bens_negocio, "bens_servicos_negocio", OUTPUT_DIR)

    # 10 — Lead (depende de paineis, pedidos, lockers e cidadaos)
    _mostrar_etapa(16, TOTAL_ETAPAS, "leads")
    leads = generate_leads(
        n=100, paineis=paineis, pedidos_bens=pedidos_bens,
        lockers=lockers, cidadaos=cidadaos, bens_servicos=bens_servicos
    )
    export_csv(leads,  "lead", OUTPUT_DIR)
    export_json(leads, "lead", OUTPUT_DIR)

    # ── NoSQL ─────────────────────────────────────────────────────────────────

    _mostrar_etapa(17, TOTAL_ETAPAS, "telemetria NoSQL")
    telemetrias = generate_locker_telemetries(
        n=200, lockers=lockers, paineis=paineis)
    export_nosql(telemetrias, "locker_telemetry", OUTPUT_DIR)

    # um log por cada doação gerada — sem n, a lista de doações define a quantidade
    _mostrar_etapa(18, TOTAL_ETAPAS, "logs financeiros NoSQL")
    financial_logs = generate_financial_logs(doacoes=doacoes)
    export_nosql(financial_logs, "financial_log", OUTPUT_DIR)

    _mostrar_etapa(19, TOTAL_ETAPAS, "logs de interacao NoSQL")
    interaction_logs = generate_interaction_logs(n=300, paineis=paineis)
    export_nosql(interaction_logs, "interaction_log", OUTPUT_DIR)

    _mostrar_etapa(20, TOTAL_ETAPAS, "notificacoes NoSQL")
    notifications = generate_notifications(n=150, leads=leads)
    export_nosql(notifications, "notification", OUTPUT_DIR)

    _mostrar_etapa(21, TOTAL_ETAPAS, "vouchers NoSQL")
    vouchers = generate_vouchers(n=100, entidades=entidades, negocios=negocios)
    export_nosql(vouchers, "vouchers", OUTPUT_DIR)

    print("\nGeracao concluida. Ficheiros atualizados na pasta output/.\n", flush=True)


if __name__ == "__main__":
    main()
