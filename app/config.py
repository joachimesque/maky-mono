from pathlib import Path

import yaml


path = Path(__file__).parents[1].joinpath('config/config.yml')


def get_config():
    with open(path, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    return cfg
