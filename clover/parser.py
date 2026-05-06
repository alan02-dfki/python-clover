from argparse import ArgumentParser
import logging
from pathlib import Path
from typing import Any, Dict

import yaml

clog = logging.getLogger(__name__)


class CloverParser:

    fn_parsers: Dict[str, ArgumentParser] = {}
    global_cfg_params: Dict[str, Any] = {}
    global_cli_params: Dict[str, Any] = {}

    def __init__(self, id: str, **kwargs):
        self.id = id
        if id in CloverParser.fn_parsers:
            self.parser = CloverParser.fn_parsers[id]
        else:
            self.parser = ArgumentParser(conflict_handler="resolve", **kwargs)
            CloverParser.fn_parsers[id] = self.parser

    @property
    def cfg_params(self):
        return CloverParser.global_cfg_params.get(self.id, {})

    @property
    def cli_params(self):
        return CloverParser.global_cli_params.get(self.id, {})

    @property
    def populated(self) -> bool:
        return self.id in CloverParser.global_cli_params

    def add_argument(self, name: str, default: Any = None, **kwargs):
        default = default if default is not None else self.cfg_params.get(name, None)
        self.parser.add_argument(self.tag_name(name), default=default, **kwargs)

    def tag_name(self, name: str):
        if name == "--":
            return name
        else:
            return f"--{self.id}.{name.strip('-')}"

    def parse(self):
        if not self.populated:
            CloverParser.global_cli_params[self.id] = vars(
                self.parser.parse_known_args()[0]
            )
        return CloverParser.global_cli_params[self.id]

    @classmethod
    def connect_config(cls, config_path: str | Path):
        """
        Params from the config file override params from code
        but not those from cli.
        Calling this method multiple times updates the config dict used by clover.
        """
        with open(config_path, "r") as yamfile:
            cfg_dct = yaml.safe_load(yamfile)

        if cfg_dct is None:
            clog.warning("Connected empty config.")
        elif "clover" not in cfg_dct:
            clog.warning("Connected confg has no clover section.")
        else:
            clover_cfg = cfg_dct["clover"]
            clog.debug(f"Adding config {clover_cfg} to clover parser.")
            for identifier, fn_params in clover_cfg.items():
                cls.global_cfg_params[identifier] = fn_params
                clover_parser = CloverParser(id=identifier)
                for p_name, p_val in fn_params.items():
                    clover_parser.add_argument(p_name, default=p_val)
