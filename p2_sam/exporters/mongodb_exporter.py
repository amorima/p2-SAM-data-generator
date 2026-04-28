import json
from pathlib import Path


def export_nosql(data: list[dict], nome: str, output_dir: Path) -> None:
    """
    Exporta uma coleção NoSQL para JSON.
    O ficheiro é prefixado com 'nosql_' para distinguir dos ficheiros SQL.
    Apaga o ficheiro existente antes de escrever.

    Args:
        data:       lista de documentos a exportar
        nome:       nome da coleção (ex: "locker_telemetry")
        output_dir: diretório de destino
    """
    if not data:
        print(f"[NoSQL] sem dados para exportar → {nome}.json")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / f"nosql_{nome}.json"
    json_path.unlink(missing_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[NoSQL] exportado ({len(data)} documentos) → {json_path}")
