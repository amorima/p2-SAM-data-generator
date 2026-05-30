import os
import subprocess
import sys
import shutil
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
TUNNELS = [
    ("3307", "localhost:3306"),   # MySQL
    ("27018", "localhost:27017")  # MongoDB
]

CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
INSTALL_DIR = Path.home() / ".cloudflared"
CLOUDFLARED_EXE = INSTALL_DIR / "cloudflared.exe"

def setup_ssh_key():
    ssh_dir = Path.home() / ".ssh"
    key_path = ssh_dir / SSH_KEY_NAME
    
    if not ssh_dir.exists():
        ssh_dir.mkdir(parents=True, exist_ok=True)
    
    if not key_path.exists():
        print(f"[*] Instalando certificado SSH em {key_path}...")
        with open(key_path, "w", newline="\n") as f:
            f.write(SSH_KEY_CONTENT.strip() + "\n")
        
        if sys.platform == "win32":
            user = os.getlogin()
            subprocess.run(["icacls", str(key_path), "/inheritance:r"], check=True, capture_output=True)
            subprocess.run(["icacls", str(key_path), "/grant:r", f"{user}:R"], check=True, capture_output=True)
        else:
            key_path.chmod(0o600)
    return str(key_path)

def install_cloudflared():
    if CLOUDFLARED_EXE.exists():
        return str(CLOUDFLARED_EXE)

    print("[*] Cloudflared não encontrado. Iniciando instalação automática...")
    if not INSTALL_DIR.exists():
        INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Fazendo download de {CLOUDFLARED_URL}...")
    try:
        urllib.request.urlretrieve(CLOUDFLARED_URL, CLOUDFLARED_EXE)
        print(f"[V] Cloudflared instalado em {CLOUDFLARED_EXE}")
    except Exception as e:
        print(f"[ERRO] Falha ao baixar cloudflared: {e}")
        return None
    
    return str(CLOUDFLARED_EXE)

def configure_ssh_config():
    ssh_config = Path.home() / ".ssh" / "config"
    entry = f"\nHost {CLOUDFLARE_HOST}\n  ProxyCommand \"{CLOUDFLARED_EXE}\" access ssh --hostname %h\n"
    
    content = ""
    if ssh_config.exists():
        with open(ssh_config, "r") as f:
            content = f.read()
    
    if CLOUDFLARE_HOST not in content:
        print(f"[*] Configurando ~/.ssh/config para túnel Cloudflare...")
        with open(ssh_config, "a") as f:
            f.write(entry)
    else:
        # Atualiza o caminho do executável caso tenha mudado
        if str(CLOUDFLARED_EXE) not in content:
            print("[*] Atualizando caminho do cloudflared no config SSH...")
            # Simplificação: apenas anexa a nova config, o SSH usa a primeira que encontrar
            with open(ssh_config, "a") as f:
                f.write(entry)

def open_tunnels(key_path):
    # Adiciona o diretório do cloudflared ao PATH do processo atual
    os.environ["PATH"] += os.pathsep + str(INSTALL_DIR)
    
    print("[*] Testando conectividade local...")
    target_host = LOCAL_IP
    ping_cmd = ["ping", "-n", "1", "-w", "500", LOCAL_IP] if sys.platform == "win32" else ["ping", "-c", "1", "-W", "1", LOCAL_IP]
    
    try:
        subprocess.run(ping_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[V] Servidor local encontrado em {LOCAL_IP}")
    except subprocess.CalledProcessError:
        print(f"[!] Servidor local offline. Mudando para Cloudflare: {CLOUDFLARE_HOST}")
        if install_cloudflared():
            configure_ssh_config()
            target_host = CLOUDFLARE_HOST
        else:
            print("[ERRO] Não foi possível usar Cloudflare sem o executável.")
            return

    ssh_cmd = ["ssh", "-i", key_path, "-o", "StrictHostKeyChecking=no"]
    for local_port, remote_dest in TUNNELS:
        ssh_cmd.extend(["-L", f"{local_port}:{remote_dest}"])
    
    ssh_cmd.extend([f"{REMOTE_USER}@{target_host}", "-N"])
    
    print(f"[*] Abrindo túneis via {target_host}...")
    print(f"    MySQL:   localhost:3307")
    print(f"    MongoDB: localhost:27018")
    
    try:
        subprocess.run(ssh_cmd)
    except KeyboardInterrupt:
        print("\n[*] Túneis fechados.")

if __name__ == "__main__":
    try:
        path = setup_ssh_key()
        open_tunnels(path)
    except Exception as e:
        print(f"\n[ERRO] {e}")
        sys.exit(1)
