import os
import sys
import getpass
import subprocess
import multiprocessing
from pathlib import Path
from gunicorn.app.base import BaseApplication
from dotenv import load_dotenv

# Load .env from the same directory
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    print(f"[WARN] .env file not found at {env_path}, using defaults")
load_dotenv(dotenv_path=env_path)

PROJECT_NAME = os.getenv("PROJECT_NAME") or "flask"
GUNICORN_FILE = os.getenv("GUNICORN_FILE") or "production_main.py"

print(f"[DEBUG] PROJECT_NAME={PROJECT_NAME}, GUNICORN_FILE={GUNICORN_FILE}")

from main import app

class GunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.app = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {k: v for k, v in self.options.items() if v is not None}
        for k, v in config.items():
            self.cfg.set(k.lower(), v)

    def load(self):
        return self.app

def create_and_deploy_service():
    project_path = Path(__file__).resolve().parent
    user = getpass.getuser()
    service_name = f"{PROJECT_NAME}.service"
    service_path = Path("/etc/systemd/system") / service_name
    gunicorn_script_path = project_path / GUNICORN_FILE

    if not gunicorn_script_path.exists():
        print(f"[ERROR] Gunicorn file not found at {gunicorn_script_path}")
        sys.exit(1)

    # Detect virtualenv python and gunicorn path
    venv_path = project_path / "venv"
    python_path = venv_path / "bin" / "python"
    gunicorn_path = venv_path / "bin" / "gunicorn"

    if not python_path.exists():
        print(f"[ERROR] Python binary not found in virtualenv at {python_path}")
        print("[ERROR] Please create a virtual environment and install dependencies before deploying.")
        sys.exit(1)

    if not gunicorn_path.exists():
        print(f"[ERROR] Gunicorn binary not found in virtualenv at {gunicorn_path}")
        print("[ERROR] Please activate the virtualenv and install gunicorn: pip install gunicorn")
        sys.exit(1)

    service_content = f"""[Unit]
Description=Gunicorn service for {PROJECT_NAME}
After=network.target

[Service]
User={user}
Group=www-data
WorkingDirectory={project_path}
ExecStart={gunicorn_path} -w 4 -b 0.0.0.0:6526 {GUNICORN_FILE.replace('.py', '')}:app
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1
Environment=PATH={venv_path}/bin:/usr/bin:/bin

[Install]
WantedBy=multi-user.target
"""

    # Overwrite existing service file (if any)
    temp_file = project_path / service_name  # Named as {project_name}.service
    temp_file.write_text(service_content)
    print(f"[INFO] Created/Overwritten temp service file at {temp_file}")

    try:
        subprocess.run(["sudo", "mv", "-f", str(temp_file), str(service_path)], check=True)  # -f to force overwrite
        subprocess.run(["sudo", "chmod", "644", str(service_path)], check=True)

        subprocess.run(["sudo", "systemctl", "daemon-reexec"], check=True)
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", service_name], check=True)
        subprocess.run(["sudo", "systemctl", "restart", service_name], check=True)  # restart to load new config

        print(f"[SUCCESS] Service {service_name} deployed and restarted!")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to deploy service: {e}")

if __name__ == "__main__":
    # Only deploy service if NOT root (run as normal user)
    if os.geteuid() != 0:
        create_and_deploy_service()

    # Start gunicorn app if run directly (not deploying service)
    workers = (2 * multiprocessing.cpu_count()) + 1
    print(f"[INFO] Running Gunicorn with {workers} workers")
    options = {
        "bind": "0.0.0.0:6526",
        "workers": workers,
        "accesslog": "-",
        "errorlog": "-",
        "loglevel": "info",
    }
    GunicornApp(app, options).run()
