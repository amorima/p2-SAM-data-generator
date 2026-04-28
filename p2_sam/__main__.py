from pathlib import Path

from p2_sam.entities.localidade.generator import generate_localidades, strip_internal_fields
from p2_sam.entities.doacao.generator import generate_mecenas
from p2_sam.entities.negocio.generator import generate_negocios
from p2_sam.entities.instituicao.generator import generate_instituicoes
from p2_sam.entities.entidade.generator import generate_entidades
from p2_sam.entities.contacto.generator import generate_contactos
from p2_sam.entities.doacao.generator import generate_doacoes
from p2_sam.entities.painel_digital.generator import generate_paineis
from p2_sam.entities.locker.generator import generate_lockers
from p2_sam.entities.cidadao.generator import generate_cidadaos
from p2_sam.entities.pedido.generator import generate_pedidos
from p2_sam.entities.bens_servicos.generator import generate_bens_servicos
from p2_sam.entities.pedido_bens_servico.generator import generate_pedidos_bens_servicos, generate_bens_servicos_negocio
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


def main() -> None:
    # 1 — Localidade (base para coordenadas)
    localidades = generate_localidades(n=100)
    codigos_postais = [loc["codigo_postal"] for loc in localidades]
    export_csv(strip_internal_fields(localidades),  "localidade", OUTPUT_DIR)
    export_json(strip_internal_fields(localidades), "localidade", OUTPUT_DIR)

    # 2 — Entidades próprias (geram os seus NIFs)
    mecenas = generate_mecenas(n=50)
    export_csv(mecenas,  "mecena", OUTPUT_DIR)
    export_json(mecenas, "mecena", OUTPUT_DIR)

    negocios = generate_negocios(n=50, localidades=localidades)
    export_csv(negocios,  "negocio", OUTPUT_DIR)
    export_json(negocios, "negocio", OUTPUT_DIR)

    instituicoes = generate_instituicoes(n=50, localidades=localidades)
    export_csv(instituicoes,  "instituicao", OUTPUT_DIR)
    export_json(instituicoes, "instituicao", OUTPUT_DIR)

    # 3 — Entidade agrega NIFs já gerados e cria email/password/iban
    entidades = generate_entidades(
        mecenas=mecenas,
        negocios=negocios,
        instituicoes=instituicoes,
        codigos_postais=codigos_postais,
    )
    export_csv(entidades,  "entidade", OUTPUT_DIR)
    export_json(entidades, "entidade", OUTPUT_DIR)

    # 4 — Contacto herda NIFs de entidade
    contactos = generate_contactos(
        entidades=entidades, contactos_por_entidade=1)
    export_csv(contactos,  "contacto", OUTPUT_DIR)
    export_json(contactos, "contacto", OUTPUT_DIR)

    # 5 — Dependem de mecenas
    doacoes = generate_doacoes(n=200, mecenas=mecenas)
    export_csv(doacoes,  "doacao", OUTPUT_DIR)
    export_json(doacoes, "doacao", OUTPUT_DIR)

    # 6 — Dispositivos físicos (dependem de localidades)
    paineis = generate_paineis(n=30, localidades=localidades)
    export_csv(paineis,  "painel_digital", OUTPUT_DIR)
    export_json(paineis, "painel_digital", OUTPUT_DIR)

    lockers = generate_lockers(n=30, localidades=localidades)
    export_csv(lockers,  "locker", OUTPUT_DIR)
    export_json(lockers, "locker", OUTPUT_DIR)

    # 7 — Sem dependências externas
    cidadaos = generate_cidadaos(n=100)
    export_csv(cidadaos,  "cidadao", OUTPUT_DIR)
    export_json(cidadaos, "cidadao", OUTPUT_DIR)

    bens_servicos = generate_bens_servicos()
    export_csv(bens_servicos,  "bens_servicos", OUTPUT_DIR)
    export_json(bens_servicos, "bens_servicos", OUTPUT_DIR)

    # 8 — Pedidos (dependem de entidades)
    pedidos = generate_pedidos(n=100, instituicoes=instituicoes)
    export_csv(pedidos,  "pedido", OUTPUT_DIR)
    export_json(pedidos, "pedido", OUTPUT_DIR)

    # 9 — Tabelas de relação
    pedidos_bens = generate_pedidos_bens_servicos(
        n=150, pedidos=pedidos, bens_servicos=bens_servicos
    )
    export_csv(pedidos_bens,  "pedido_bens_servicos", OUTPUT_DIR)
    export_json(pedidos_bens, "pedido_bens_servicos", OUTPUT_DIR)

    bens_negocio = generate_bens_servicos_negocio(
        n=100, negocios=negocios, bens_servicos=bens_servicos
    )
    export_csv(bens_negocio,  "bens_servicos_negocio", OUTPUT_DIR)
    export_json(bens_negocio, "bens_servicos_negocio", OUTPUT_DIR)

    # 10 — Lead (depende de paineis, pedidos, lockers e cidadaos)
    leads = generate_leads(
        n=100, paineis=paineis, pedidos=pedidos,
        lockers=lockers, cidadaos=cidadaos
    )
    export_csv(leads,  "lead", OUTPUT_DIR)
    export_json(leads, "lead", OUTPUT_DIR)

    # ── NoSQL ─────────────────────────────────────────────────────────────────

    telemetrias = generate_locker_telemetries(
        n=200, lockers=lockers, paineis=paineis)
    export_nosql(telemetrias, "locker_telemetry", OUTPUT_DIR)

    # um log por cada doação gerada — sem n, a lista de doações define a quantidade
    financial_logs = generate_financial_logs(doacoes=doacoes)
    export_nosql(financial_logs, "financial_log", OUTPUT_DIR)

    interaction_logs = generate_interaction_logs(n=300, paineis=paineis)
    export_nosql(interaction_logs, "interaction_log", OUTPUT_DIR)

    notifications = generate_notifications(n=150, leads=leads)
    export_nosql(notifications, "notification", OUTPUT_DIR)

    vouchers = generate_vouchers(n=100, entidades=entidades, negocios=negocios)
    export_nosql(vouchers, "vouchers", OUTPUT_DIR)


if __name__ == "__main__":
    main()
