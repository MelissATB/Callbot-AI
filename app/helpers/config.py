# Load "CONFIG_JSON" for debug purposes
from dotenv import load_dotenv, find_dotenv

# Load recursively from relative, like "config.yaml"
load_dotenv(find_dotenv())

# Load deps
from helpers.config_models.root import RootModel
from os import environ
from pydantic import ValidationError
import yaml
from typing import Optional


_CONFIG_ENV = "CONFIG_JSON"
_CONFIG_FILE = "../../infra/configs/config.yaml"


class ConfigNotFound(Exception):
    pass


class ConfigBadFormat(Exception):
    pass


def load_config() -> RootModel:
    config: Optional[RootModel] = None
    config_env = "CONFIG_JSON"
    config_file = "../../configs/config.yaml"

    if config_env in environ:
        config = RootModel.model_validate_json(environ[config_env])
        print(f'Config loaded from env "{config_env}"')
        return config

    print(f'Cannot find env "{config_env}", trying to load from file')
    path = find_dotenv(filename=config_file)
    if not path:
        raise ConfigNotFound(f'Cannot find config file "{config_file}"')
    try:
        with open(
            encoding="utf-8",
            file=path,
            mode="r",
        ) as f:
            config = RootModel.model_validate(yaml.safe_load(f))
            print(f'Config loaded from file "{path}"')
            return config
    except ValidationError as e:
        raise ConfigBadFormat("Config values are not valid") from e
    except Exception as e:
        raise ConfigBadFormat("Config YAML format is not valid") from e


CONFIG = load_config()
