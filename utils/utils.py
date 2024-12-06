def load_config():
    config_file = "ow.config"
    config = {}
    with open(config_file, "r") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip().strip('"')
    return config