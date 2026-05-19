import csv
from pathlib import Path


def export_csv(data: list[dict], nome: str, output_dir: Path) -> None:
    """
    Exporta uma lista de dicionários para um ficheiro CSV
    Apaga o ficheiro existente antes de escrever

    Argumentos:
        data:       lista de registos a exportar
        nome:       nome base do ficheiro (sem extensão)
        output_dir: diretório de destino
    """
    if not data:
        print(f"[CSV]  sem dados para exportar → {nome}.csv")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / f"{nome}.csv"
    csv_path.unlink(missing_ok=True)

    fieldnames = list(dict.fromkeys(key for row in data for key in row.keys()))

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"[CSV]  exportado ({len(data)} registos) → {csv_path}")
