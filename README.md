# Phase 10 Randomizer Web App

This repo hosts a Phase 10 randomizer web app with:

* A PHP front-end that renders the page and calls a Python backend.
* A Python backend (Flask) that generates and ranks Phase 10 phases.
* A shared `phase10config.json` so you can tune things like Monte Carlo trials, phase constraints, and timeouts from the UI.

It’s designed to run:

* In dev on a single Windows box with PHP’s built-in server and a local Flask server.
* In prod on a Synology NAS using Docker, with:

  * `nginx` as the edge reverse proxy (separate container).
  * `php-fpm` for the PHP front-end.
  * `py-app` for the Python backend (gunicorn + Flask), all sharing `/volume1/docker/www`.

---

## Directory layout

Place the full project inside a folder called `phase10`.

Typical structure (on dev or on the NAS under `/volume1/docker/www/phase10`):

```
phase10/
  index.php
  main.css
  python_client.php
  phase10_html.py
  phase10_service.py
  phase10config.py
  phase10config.json
  phase10logic.py
  phase10probability.py
  phase10typelogic.py
  requirements.txt
  images/
    phase10icon.png
    phase10logo.png
```

Component purposes:

* **index.php** – main web page and settings UI (gear icon).
* **main.css** – styling for the page and settings panel.
* **python_client.php** – talks to the Python backend via HTTP.
* **phase10_html.py** – the standalone “engine” that prints a `<li>` list.
* **phase10_service.py** – Flask service with `/health` and `/phase10/html`.
* **phase10config.* ** – default config, merged values, and runtime settings.
* **phase10logic/probability/typelogic** – the actual phase generator.
* **requirements.txt** – Python dependencies.
* **images/** – icons and logo used in the interface.

---

## Development setup (Windows)

### 1. Python environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Start Python backend

```bash
.\.venv\Scripts\activate
python phase10_service.py
```

This starts:

```
http://127.0.0.1:5001
```

### 3. Start PHP dev server

```bash
php -S localhost:8000 -t .
```

Browse to:

```
http://localhost:8000/
```

`python_client.php` automatically chooses `http://127.0.0.1:5001` in dev.

---

## Config and settings

Configuration is stored in **phase10config.json** and automatically updated via UI.
Each request merges:

1. Defaults from `phase10config.py`
2. Saved JSON values
3. Query parameters from the UI gear panel

Then it writes the updated JSON back to disk.

### **Config key descriptions**

* **MC_TRIALS_DEFAULT**
  Number of Monte Carlo trials. Higher = more accurate, slower.

* **PHASE_PROB_CACHE**
  Stored as `{}` in JSON; live cache handled internally.

* **COLOR_RAND**
  Weight for generating color-based phase components.

* **WILD_RAND**
  Weight for generating wild-heavy components.

* **TYPE_MAX_PER_PHASE**
  How many different *types* can appear in a single phase.
  (Set to **1** to prevent duplicates like multiple runs, multiple even/odd, etc.)

* **USE_MONTE_CARLO**
  `true` enables Monte Carlo simulation.

* **SHOW_PHASE_PROBABILITY**
  Whether probability numbers appear beside each phase.

* **MIN_CARDS_PER_PHASE**
  Minimum cards required for a phase to be valid.

* **TYPE_MAX_PER_TYPE_GLOBAL**
  How many times a given type may appear across all 10 phases.

* **HTML_TIMEOUT_SECONDS**
  Maximum time allowed for `phase10_html.py` to run.
  If exceeded, a clean `<li>` timeout message is returned.

---

## Production setup (Synology + Docker)

### 1. Place code here on the NAS:

```
/volume1/docker/www/phase10
```

### 2. Python backend container (`py-app`)

This image is generic and loads the project from the mounted `/www`.

#### wsgi.py

Located in `/volume1/docker/pyapp/wsgi.py`:

```python
import os
import sys

APP_DIR = os.environ.get("APP_DIR", "/www/phase10")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from phase10_service import app
```

#### Dockerfile (py-app)

```dockerfile
FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=America/New_York

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wsgi.py /app/wsgi.py

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app",
     "--workers=1",
     "--threads=1",
     "--timeout=120",
     "--graceful-timeout=120"]
```

---

# **Worker configuration (Gunicorn)**

*(Merged and finalized)*

The production Python backend uses **Gunicorn**.
To avoid intermittent timeouts caused by Monte Carlo generation on NAS hardware, we run:

* **1 worker**
* **1 thread**
* **120s timeout**

This avoids worker churn, resource contention, and dropped requests.

### Updated Gunicorn command

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app",
     "--workers=1",
     "--threads=1",
     "--timeout=120",
     "--graceful-timeout=120"]
```

### Why this works

* Synology hardware has lower single-core performance than your dev machine.
* The Phase 10 generator (especially with Monte Carlo) is CPU-intensive.
* Too many workers/threads = random timeouts + 0-byte responses to PHP.
* A single worker guarantees stable performance.

You may raise:

* `--threads` to 2 or
* `MC_TRIALS_DEFAULT`
* `HTML_TIMEOUT_SECONDS`

if your NAS is upgraded, but the defaults above are ideal for DS1815+.

---

## php-fpm snippet

```yaml
services:
  php:
    image: php:fpm-alpine
    container_name: php-fpm
    restart: unless-stopped
    environment:
      - TZ=America/New_York
      - PHASE10_BASE_URL=http://py:8000
    volumes:
      - /volume1/docker/nginx/html:/var/www/html
    networks:
      apps: {}
```

---

## nginx snippet

```nginx
server {
    listen 443 ssl http2;
    server_name phase10.example.com;

    root /var/www/html/phase10;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass php-fpm:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
```

---

# **Monte Carlo tuning**

On NAS hardware:

* Use `TYPE_MAX_PER_PHASE = 1` to avoid duplicate components in a phase
* Set `MC_TRIALS_DEFAULT = 1000–1500`
* Set `HTML_TIMEOUT_SECONDS = 8–12`
* Leave `USE_MONTE_CARLO = true`

This gives excellent performance and still provides probability values.

---

# License

This project is licensed under the MIT License.
See the `LICENSE` file for full terms.

---

# Trademarks

* **Phase 10** is a registered trademark of Mattel, Inc.
  This project is an independent, fan-made tool.
* **Python** is a trademark of the Python Software Foundation.
* **PHP**, **Docker**, **Synology**, and other names are trademarks of their respective owners.

---
