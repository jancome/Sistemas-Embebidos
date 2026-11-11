"""Ejecutar en la Raspberry, desde su usuario normal y el entorno .venv."""
from pathlib import Path
import os
import pwd

ROOT = Path(__file__).resolve().parent
if os.getuid() == 0:
    raise SystemExit("Ejecutar como usuario normal, sin sudo.")
usuario = pwd.getpwuid(os.getuid()).pw_name
python = ROOT / ".venv/bin/python"
if not python.exists():
    raise SystemExit("Crear primero el entorno .venv junto a app.py.")

service = f"""[Unit]
Description=Monitor ESP32 y dashboard local
After=local-fs.target

[Service]
Type=simple
User={usuario}
SupplementaryGroups=dialout
WorkingDirectory="{ROOT}"
ExecStart="{python}" "{ROOT / 'app.py'}"
Environment=PYTHONUNBUFFERED=1
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
"""
destino = ROOT / "monitor-esp32.service"
destino.write_text(service)
print("Archivo generado:", destino)
print("Instalar con los comandos indicados en la guía.")
