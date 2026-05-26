import random
from faker import Faker
from p2_sam.utils.dates import data_organica_iso

faker = Faker("pt_PT")

EVENTOS = ["HEARTBEAT", "OVERHEAT", "ERRO_SENSOR",
           "ERRO_SISTEMA", "PORTA_ABERTA", "PORTA_FECHADA"]
TIPOS_DISPOSITIVO = ["LOCKER", "PAINEL"]
AVISOS = ["NENHUM", "TEMPERATURA_ALTA",
          "BATERIA_BAIXA", "SINAL_FRACO", "FALHA_SENSOR"]


def generate_locker_telemetry(lockers: list[dict], paineis: list[dict]) -> dict:
    """
    Gera um evento de telemetria de um locker ou painel.
    locker_id referencia o id_locker da tabela SQL locker_inteligente.
    """
    usar_locker = random.choice([True, False])

    if usar_locker:
        dispositivo = random.choice(lockers)
        dispositivo_id = dispositivo["id_locker"]
        tipo = "LOCKER"
        lat = dispositivo["geo_latitude"]
        lon = dispositivo["geo_longitude"]
    else:
        dispositivo = random.choice(paineis)
        dispositivo_id = dispositivo["id_dispositivo"]
        tipo = "PAINEL"
        lat = dispositivo["geo_latitude"]
        lon = dispositivo["geo_longitude"]

    evento = random.choices(
        EVENTOS,
        weights=[60, 5, 10, 10, 7, 8],
        k=1
    )[0]

    bateria = round(random.uniform(10.0, 14.8), 1)
    cpu_temp = round(random.uniform(30.0, 80.0), 1)
    aviso = "NENHUM"

    if cpu_temp > 60:
        aviso = "TEMPERATURA_ALTA"
    elif bateria < 11.5:
        aviso = "BATERIA_BAIXA"
    elif random.random() < 0.05:
        aviso = random.choice(["SINAL_FRACO", "FALHA_SENSOR"])

    return {
        "timestamp": data_organica_iso(),
        "evento": evento,
        "locker_id": dispositivo_id,
        "tipo": tipo,
        "geo_latitude": lat,
        "geo_longitude": lon,
        "bateria_estado": bateria,
        "cpu_temperatura": cpu_temp,
        "dmb_sinal": round(random.uniform(-90.0, -40.0), 1),
        "aviso": aviso,
        "status": {
            "sensor_porta": random.choice(["OK", "FALHA"]),
            "numpad": random.choice(["OK", "FALHA"]),
        },
        "versao": f"v{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
    }


def generate_locker_telemetries(n: int = 200, lockers: list[dict] = None,
                                paineis: list[dict] = None) -> list[dict]:
    if not lockers or not paineis:
        raise ValueError("É necessário fornecer lockers e paineis.")

    resultados = []

    print(f"A gerar {n} eventos de telemetria...\n")

    for _ in range(n):
        resultados.append(generate_locker_telemetry(lockers, paineis))

    print(f"  Concluído! {len(resultados)} eventos de telemetria gerados.\n")
    return resultados
