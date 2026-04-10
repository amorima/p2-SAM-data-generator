import json
from pathlib import Path


def export_json(data: list[dict], nome: str, output_dir: Path) -> None:
    """
    Exporta uma lista de dicionários para um ficheiro JSON.
    Apaga o ficheiro existente antes de escrever.

    Args:
        data:       lista de registos a exportar
        nome:       nome base do ficheiro (sem extensão)
        output_dir: diretório de destino
    """
    if not data:
        print(f"[JSON] sem dados para exportar → {nome}.json")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / f"{nome}.json"
    json_path.unlink(missing_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[JSON] exportado ({len(data)} registos) → {json_path}")