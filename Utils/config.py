import yaml

def load_config(config_path: str) -> dict:
    """
    Load YAML configuration into a Python dictionary.
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[!] Failed to load config file: {e}")
        return {}