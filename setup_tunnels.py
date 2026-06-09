"""Script para configurar túneis SSH e gerir seeds da base de dados do SAM."""

import os
import sys
import time
import shutil
import socket
import argparse
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

# --- CONFIGURAÇÃO ---
SSH_KEY_NAME = "sam_tunnel"
SSH_KEY_CONTENT = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACCCOBHrwVR5nVgOAhrL0AR0+glASZWEkctz+r4ZEqgucgAAAJi+SR8Pvkkf
DwAAAAtzc2gtZWQyNTUxOQAAACCCOBHrwVR5nVgOAhrL0AR0+glASZWEkctz+r4ZEqgucg
AAAEAtSzvkq/xkh0euwZ/OJ9Ydlh5jvnShfk57bdbuxXpr4II4EevBVHmdWA4CGsvQBHT6
CUBJlYSRy3P6vhkSqC5yAAAAD3NhbS1zZWVkLXR1bm5lbAECAwQFBg==
-----END OPENSSH PRIVATE KEY-----"""

REMOTE_USER = "antonio"
LOCAL_IP = "192.168.188.102"
CLOUDFLARE_HOST = "ssh.netdw.tech"

# Mapeamento de portos: Local -> Remoto
TUNNELS = [("3307", "localhost:3306"), ("27018", "localhost:27017")]  # MySQL  # MongoDB

# Endpoints locais que o seed deve usar (derivados de TUNNELS, não do .env).
MYSQL_LOCAL_PORT = TUNNELS[0][0]
MONGO_LOCAL_PORT = TUNNELS[1][0]
MONGO_REMOTE_PORT = TUNNELS[1][1].rsplit(":", 1)[1]

REPO_ROOT = Path(__file__).resolve().parent
ENV_PATH = REPO_ROOT / ".env"
DATABASE_DIR = REPO_ROOT / "p2_sam" / "database"

CLOUDFLARED_URL = (
    "https://github.com/cloudflare/cloudflared/releases/latest/download/"
    "cloudflared-windows-amd64.exe"
)
INSTALL_DIR = Path.home() / ".cloudflared"
CLOUDFLARED_EXE = INSTALL_DIR / "cloudflared.exe"


def setup_ssh_key():
    """Cria o ficheiro de chave SSH privada em ~/.ssh e ajusta as permissões."""
    ssh_dir = Path.home() / ".ssh"
    key_path = ssh_dir / SSH_KEY_NAME

    if not ssh_dir.exists():
        ssh_dir.mkdir(parents=True, exist_ok=True)

    if not key_path.exists():
        print(f"[*] Instalando certificado SSH em {key_path}...")
        with open(key_path, "w", newline="\n", encoding="utf-8") as f:
            f.write(SSH_KEY_CONTENT.strip() + "\n")

        if sys.platform == "win32":
            user = os.getlogin()
            subprocess.run(
                ["icacls", str(key_path), "/inheritance:r"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["icacls", str(key_path), "/grant:r", f"{user}:R"],
                check=True,
                capture_output=True,
            )
        else:
            key_path.chmod(0o600)
    return str(key_path)


def install_cloudflared():
    """Descarrega e instala o cloudflared se ainda não existir.

    Devolve o caminho ou None em caso de erro.
    """
    if CLOUDFLARED_EXE.exists():
        return str(CLOUDFLARED_EXE)

    print("[*] Cloudflared não encontrado. Iniciando instalação automática...")
    if not INSTALL_DIR.exists():
        INSTALL_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[*] Fazendo download de {CLOUDFLARED_URL}...")
    try:
        urllib.request.urlretrieve(CLOUDFLARED_URL, CLOUDFLARED_EXE)
        print(f"[V] Cloudflared instalado em {CLOUDFLARED_EXE}")
    except (OSError, urllib.error.URLError) as e:
        print(f"[ERRO] Falha ao baixar cloudflared: {e}")
        return None

    return str(CLOUDFLARED_EXE)


def configure_ssh_config():
    """Adiciona (ou atualiza) a entrada ProxyCommand do cloudflared no ~/.ssh/config."""
    ssh_config = Path.home() / ".ssh" / "config"
    entry = (
        f"\nHost {CLOUDFLARE_HOST}\n"
        f'  ProxyCommand "{CLOUDFLARED_EXE}" access ssh --hostname %h\n'
    )

    content = ""
    if ssh_config.exists():
        with open(ssh_config, "r", encoding="utf-8") as f:
            content = f.read()

    if CLOUDFLARE_HOST not in content:
        print("[*] Configurando ~/.ssh/config para túnel Cloudflare...")
        with open(ssh_config, "a", encoding="utf-8") as f:
            f.write(entry)
    else:
        # Atualiza o caminho do executável caso tenha mudado
        if str(CLOUDFLARED_EXE) not in content:
            print("[*] Atualizando caminho do cloudflared no config SSH...")
            # Simplificação: apenas anexa a nova config, o SSH usa a primeira que encontrar
            with open(ssh_config, "a", encoding="utf-8") as f:
                f.write(entry)


def port_listening(port, host="127.0.0.1"):
    """True se já há algo à escuta no porto local (túnel possivelmente aberto)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, int(port))) == 0


def wait_for_ports(ports, timeout=40):
    """Espera até todos os portos locais estarem à escuta, ou expira."""
    print(f"[*] A aguardar que os portos {', '.join(ports)} fiquem disponíveis...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        if all(port_listening(p) for p in ports):
            print("[V] Túnel pronto.")
            return True
        time.sleep(1)
    print("[ERRO] Tempo esgotado à espera do túnel.")
    return False


def open_tunnels(key_path):
    """Abre o túnel SSH em background. Devolve o processo (ou None se já estava aberto)."""
    # Adiciona o diretório do cloudflared ao PATH do processo atual
    os.environ["PATH"] += os.pathsep + str(INSTALL_DIR)

    local_ports = [local for local, _ in TUNNELS]
    if all(port_listening(p) for p in local_ports):
        print("[V] Túnel já estava aberto (portos à escuta). A reutilizar.")
        return None

    print("[*] Testando conectividade local...")
    target_host = LOCAL_IP
    ping_cmd = (
        ["ping", "-n", "1", "-w", "500", LOCAL_IP]
        if sys.platform == "win32"
        else ["ping", "-c", "1", "-W", "1", LOCAL_IP]
    )

    try:
        subprocess.run(
            ping_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print(f"[V] Servidor local encontrado em {LOCAL_IP}")
    except subprocess.CalledProcessError:
        print(f"[!] Servidor local offline. Mudando para Cloudflare: {CLOUDFLARE_HOST}")
        if install_cloudflared():
            configure_ssh_config()
            target_host = CLOUDFLARE_HOST
        else:
            print("[ERRO] Não foi possível usar Cloudflare sem o executável.")
            return None

    ssh_cmd = ["ssh", "-i", key_path, "-o", "StrictHostKeyChecking=no"]
    for local_port, remote_dest in TUNNELS:
        ssh_cmd.extend(["-L", f"{local_port}:{remote_dest}"])

    ssh_cmd.extend([f"{REMOTE_USER}@{target_host}", "-N"])

    print(f"[*] Abrindo túneis via {target_host}...")
    print(f"    MySQL:   localhost:{MYSQL_LOCAL_PORT}")
    print(f"    MongoDB: localhost:{MONGO_LOCAL_PORT}")

    # Background: não bloqueia, para podermos correr o seed a seguir.
    return subprocess.Popen(ssh_cmd)


def read_env_value(key):
    """Lê um valor do .env da raiz (sem depender de libs externas)."""
    if not ENV_PATH.exists():
        return None
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#") or "=" not in trimmed:
            continue
        k, _, v = trimmed.partition("=")
        if k.strip() == key:
            return v.strip().strip('"').strip("'")
    return None


def build_seed_env():
    """
    Ambiente para os comandos de seed: força host/porta do túnel.
    O config/database.js só usa o .env quando a variável ainda não existe,
    por isso estes overrides ganham. As credenciais (DB_USER/PASSWORD/NAME,
    e auth do Mongo) continuam a vir do .env.
    """
    env = os.environ.copy()
    env["DB_HOST"] = "127.0.0.1"
    env["DB_PORT"] = MYSQL_LOCAL_PORT

    mongo_uri = read_env_value("MONGODB_URI")
    if mongo_uri:
        # Reescreve só o porto remoto (27017) para o porto local do túnel (27018).
        env["MONGODB_URI"] = mongo_uri.replace(
            f":{MONGO_REMOTE_PORT}", f":{MONGO_LOCAL_PORT}"
        )

    # Evita o crash de encoding cp1252 em consolas Windows.
    env.setdefault("PYTHONIOENCODING", "utf-8")
    return env


def _node_tool(name):
    """Resolve npx/npm (com .cmd no Windows)."""
    if sys.platform == "win32":
        return shutil.which(name) or shutil.which(f"{name}.cmd") or f"{name}.cmd"
    return shutil.which(name) or name


def run_step(label, cmd, cwd, env):
    """Corre um comando, faz log e devolve True/False conforme o código de saída."""
    print(f"\n[*] {label}: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(cwd), env=env, check=False)
    if result.returncode != 0:
        print(f"[ERRO] {label} falhou (código {result.returncode}).")
        return False
    print(f"[V] {label} concluído.")
    return True


def _python_for_generator():
    """
    Devolve o Python do .venv do projeto (onde estão instaladas as deps do
    gerador, ex.: pgeocode). Cai para sys.executable se não existir — mas o
    interpretador que lança este script pode não ter as deps (ex.: Python da
    Windows Store), por isso o .venv é preferido.
    """
    candidates = [
        REPO_ROOT / ".venv" / "Scripts" / "python.exe",  # Windows
        REPO_ROOT / ".venv" / "bin" / "python",  # POSIX
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return sys.executable


def run_generator(env):
    """Gera os ficheiros sintéticos em output/ (python -m p2_sam)."""
    return run_step(
        "Gerador", [_python_for_generator(), "-m", "p2_sam"], REPO_ROOT, env
    )


def run_migrations(env):
    """Corre as migrations do Sequelize para garantir o schema MySQL atualizado."""
    if not DATABASE_DIR.exists():
        print(f"[ERRO] Pasta de base de dados não encontrada: {DATABASE_DIR}")
        return False
    return run_step(
        "Migrations",
        [_node_tool("npx"), "sequelize-cli", "db:migrate"],
        DATABASE_DIR,
        env,
    )


def seed_mysql(env):
    """Garante o schema (migrations) e semeia o MySQL."""
    if not DATABASE_DIR.exists():
        print(f"[ERRO] Pasta de base de dados não encontrada: {DATABASE_DIR}")
        return False
    if not run_migrations(env):
        return False
    return run_step(
        "Seed MySQL", [_node_tool("npm"), "run", "seed:sql"], DATABASE_DIR, env
    )


def seed_mongodb(env):
    """Semeia a base de dados MongoDB via npm run seed:nosql."""
    if not DATABASE_DIR.exists():
        print(f"[ERRO] Pasta de base de dados não encontrada: {DATABASE_DIR}")
        return False
    return run_step(
        "Seed MongoDB", [_node_tool("npm"), "run", "seed:nosql"], DATABASE_DIR, env
    )


def seed_all(env):
    """Corre seed_mysql seguido de seed_mongodb; aborta se o primeiro falhar."""
    return seed_mysql(env) and seed_mongodb(env)


MENU_OPTIONS = [
    ("1", "Gerador", run_generator),
    ("2", "Seed MongoDB", seed_mongodb),
    ("3", "Seed MySQL", seed_mysql),
    ("4", "Seed All", seed_all),
    ("5", "Quit", None),
]


def menu_loop(env):
    """Mostra o menu em loop até o utilizador escolher Quit."""
    while True:
        print("\n" + "=" * 32)
        print("  SAM — Túnel ativo. Escolhe uma opção:")
        print("=" * 32)
        for key, label, _ in MENU_OPTIONS:
            print(f"  {key}) {label}")

        try:
            choice = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n[*] A sair.")
            return

        action = None
        for key, label, fn in MENU_OPTIONS:
            if choice == key or choice == label.lower():
                action = (label, fn)
                break

        if action is None:
            print("[!] Opção inválida.")
            continue

        label, fn = action
        if fn is None:  # Quit
            print("[*] A sair.")
            return

        try:
            fn(env)
        except KeyboardInterrupt:
            print(f"\n[!] {label} interrompido.")


def main():
    """Ponto de entrada: configura o túnel SSH e lança o menu interativo (ou modo --no-menu)."""
    parser = argparse.ArgumentParser(
        description="Abre o túnel SSH para o SAM e mostra um menu (gerador / seeds)."
    )
    parser.add_argument(
        "--no-menu",
        action="store_true",
        help="Apenas abre o túnel e mantém-no aberto (sem menu).",
    )
    args = parser.parse_args()

    proc = None
    try:
        key_path = setup_ssh_key()
        proc = open_tunnels(key_path)

        local_ports = [local for local, _ in TUNNELS]
        if not wait_for_ports(local_ports):
            return 1

        if args.no_menu:
            print("\n[*] Modo --no-menu: túnel aberto. Ctrl+C para fechar.")
            if proc is not None:
                proc.wait()
            else:
                # Túnel reutilizado: nada para aguardar, bloqueia até Ctrl+C.
                while True:
                    time.sleep(3600)
            return 0

        menu_loop(build_seed_env())
        return 0
    except KeyboardInterrupt:
        print("\n[*] Interrompido pelo utilizador.")
        return 0
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"\n[ERRO] {e}")
        return 1
    finally:
        # Fecha o túnel que nós abrimos (não mexe num que já estivesse aberto).
        if proc is not None and proc.poll() is None:
            print("[*] A fechar o túnel...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    sys.exit(main())
