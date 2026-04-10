import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import math
import json
import csv
import time
from pathlib import Path
from faker import Faker
import pgeocode

# Configuração 

faker      = Faker("pt_PT")
geo        = pgeocode.Nominatim("PT")
OUTPUT_DIR = Path(__file__).parent.parent / "output_teste"
N          = 100    # Queremos 100 dados de localidade 

# Geração 

def generate_postal_code() -> dict | None:
    """
    Gera um código postal no formato XXXX-XXX com Faker e valida-o
    contra a base GeoNames via pgeocode.
    Apos testes com a função numerify e postcode, foi possivel observar que a taxa 
    de sucesso é bastante similar, decidi usar postcode já que é a nativa para 
    gerar codigos postais e a eficiência nao altera
    A rua é gerada pelo Faker dado que o GeoNames não tem dados ao nível de rua.

    Devolve um dict com todos os campos preenchidos, ou None se o
    código gerado não existir na base de dados.
    """
    # cp = faker.numerify(text="####-###")
    # r  = geo.query_postal_code(cp)
    cp = faker.postcode()
    r  = geo.query_postal_code(cp)
    nPorta = faker.numerify("##")

    if math.isnan(r["latitude"]) or math.isnan(r["longitude"]):
        return None

    return {
        "codigo_postal" : cp,
        "rua"           : faker.street_name(),
        "freguesia"     : r["place_name"]  if isinstance(r["place_name"],  str) else None,
        "concelho"      : r["county_name"] if isinstance(r["county_name"], str) else None,
        "distrito"      : r["state_name"]  if isinstance(r["state_name"],  str) else None,
        "latitude"      : round(float(r["latitude"]),  6),
        "longitude"     : round(float(r["longitude"]), 6),
        "pais"          : "Portugal",
        "nº de porta"   : nPorta,
    }

def generate_postal_codes(n: int = N) -> list[dict]:
    """
    Gera n códigos postais válidos com contador de progresso e tempo.
    Códigos que não existam na base GeoNames são descartados e regenerados.
    """
    resultados     = []
    tentativas     = 0
    codigos_vistos = set()
    inicio         = time.time()

    print(f"A gerar {n} códigos postais válidos...\n")

    while len(resultados) < n:
        tentativas += 1
        registo = generate_postal_code()

        if registo is None:
            continue

        cp = registo["codigo_postal"]
        if cp in codigos_vistos:
            continue

        codigos_vistos.add(cp)
        resultados.append(registo)

        # progresso a cada 10 registos
        if len(resultados) % 10 == 0:
            decorrido = time.time() - inicio
            print(f"  {len(resultados):>3}/{n}  |  {tentativas} tentativas  |  {decorrido:.1f}s decorridos")

    total = time.time() - inicio
    minutos, segundos = divmod(total, 60)

    print(f"\n{'─' * 50}")
    print(f"  Concluído!")
    print(f"  Registos válidos : {len(resultados)}")
    print(f"  Total tentativas : {tentativas}")
    print(f"  Taxa de sucesso  : {len(resultados) / tentativas * 100:.1f}%")
    if minutos > 0:
        print(f"  Tempo total      : {int(minutos)}m {segundos:.1f}s")
    else:
        print(f"  Tempo total      : {segundos:.1f}s")
    print(f"{'─' * 50}\n")

    return resultados

# Exportação 

def export(data: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = OUTPUT_DIR / "localidade.json"
    json_path.unlink(missing_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[JSON] exportado → {json_path}")

    csv_path = OUTPUT_DIR / "localidade.csv"
    csv_path.unlink(missing_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"[CSV]  exportado → {csv_path}")

# Main 

if __name__ == "__main__":
    dados = generate_postal_codes(N)
    export(dados)

    print("\nExemplo dos primeiros 3 registos:")
    print(json.dumps(dados[:3], ensure_ascii=False, indent=2))