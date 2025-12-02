import json
import os

_DEFAULTS = {
    "MC_TRIALS_DEFAULT": 5000,
    "PHASE_PROB_CACHE": {},
    "COLOR_RAND": 8,
    "WILD_RAND": 20,
    "TYPE_MAX_PER_PHASE": 2,
    "USE_MONTE_CARLO": True,
    "SHOW_PHASE_PROBABILITY": True,
    "MIN_CARDS_PER_PHASE": 6,
    "TYPE_MAX_PER_TYPE_GLOBAL": 2,
    "HTML_TIMEOUT_SECONDS": 5,
    "MC_SERVICE_TRIALS": 20000,
    "MC_WORKER_INTERVAL_SECONDS": 300
}


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "phase10config.json")
    cfg = {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        cfg = {}
    except Exception:
        # If config is broken, fall back to defaults
        cfg = {}

    merged = dict(_DEFAULTS)
    for key, value in cfg.items():
        if key in merged:
            merged[key] = value
    return merged


CONFIG = load_config()
