from pathlib import Path

from p2_sam.entities.localidade.generator  import generate_localidades, strip_internal_fields
from p2_sam.entities.instituicao.generator import generate_instituicoes
from p2_sam.entities.mecena.generator      import generate_mecenas
from p2_sam.entities.doacao.generator      import generate_doacoes
from p2_sam.exporters.csv_exporter         import export_csv
from p2_sam.exporters.json_exporter        import export_json

OUTPUT_DIR = Path(__file__).parent.parent / "output"


def main() -> None:
    # Localidade 
    # Gera com campos internos (_latitude, _longitude) para uso por outras entidades
    localidades = generate_localidades(n=100)
    export_csv(strip_internal_fields(localidades),  "localidade", OUTPUT_DIR)
    export_json(strip_internal_fields(localidades), "localidade", OUTPUT_DIR)

    # Instituição 
    # Herda codigo_postal e coordenadas reais das localidades geradas
    instituicoes = generate_instituicoes(n=50, localidades=localidades)
    export_csv(instituicoes,  "instituicao", OUTPUT_DIR)
    export_json(instituicoes, "instituicao", OUTPUT_DIR)

    # Mecena 
    mecenas = generate_mecenas(n=50)
    export_csv(mecenas,  "mecena", OUTPUT_DIR)
    export_json(mecenas, "mecena", OUTPUT_DIR)

    # Doação 
    doacoes = generate_doacoes(n=200, mecenas=mecenas)
    export_csv(doacoes,  "doacao", OUTPUT_DIR)
    export_json(doacoes, "doacao", OUTPUT_DIR)


if __name__ == "__main__":
    main()