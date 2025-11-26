import sys
import os
import uuid
import hashlib
import json
import socket
import platform
from datetime import datetime
from urllib.request import urlopen, Request


def get_public_ip():
    """Vrátí veřejnou IP pomocí api.ipify.org."""
    try:
        with urlopen("https://api.ipify.org?format=json", timeout=5) as r:
            return json.loads(r.read().decode()).get("ip", "Unknown")
    except Exception:
        return "Unknown"


def get_local_ip():
    """Vrátí lokální IP adresu."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unknown"


def get_folder_hash(folder):
    """
    Vytvoří hash názvu složky a časů jejího vytvoření.
    Chrání proti obcházení úkolu změnou názvu nebo kopírováním hotového projektu.
    """
    folder_name = os.path.basename(folder)

    try:
        stat = os.stat(folder)
        meta = f"{folder_name}|{stat.st_ctime}|{stat.st_mtime}"
    except Exception:
        meta = folder_name

    return hashlib.sha256(meta.encode("utf-8")).hexdigest()


def generate_unique_token():
    """Vytvoří unikátní token vázaný na počítač a aktuální čas."""
    raw = f"{uuid.uuid4()}|{platform.node()}|{datetime.now().timestamp()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def system_info():
    """Vrátí slovník se systémovými informacemi."""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    output_file = os.path.join(base_dir, "project_proof.json")

    proof = {
        "timestamp": datetime.now().isoformat(),
        "project_folder": base_dir,
        "project_folder_hash": get_folder_hash(base_dir),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "public_ip": get_public_ip(),
        "local_ip": get_local_ip(),
        "unique_token": generate_unique_token(),
        "system_info": system_info(),
    }

    # Uložení důkazů
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(proof, f, indent=4, ensure_ascii=False)

    print("Důkazní soubor 'project_proof.json' byl úspěšně vytvořen.")
    print("Python interpreter:", sys.executable)


if __name__ == "__main__":
    main()