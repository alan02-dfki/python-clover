import logging
from pathlib import Path

from ..decorator import clover, connect_config


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@clover
def configured_fn(
    code_only,
    config_only,
    cli_only,
    code_and_config,
    config_and_cli,
    code_and_cli,
    code_config_and_cli,
):
    args = {
        "code_only": code_only,
        "config_only": config_only,
        "cli_only": cli_only,
        "code_and_config": code_and_config,
        "config_and_cli": config_and_cli,
        "code_and_cli": code_and_cli,
        "code_config_and_cli": code_config_and_cli,
    }

    for k, v in args.items():
        log.info(f"arg {k.ljust(20)} assumed value {v}.")


if __name__ == "__main__":
    connect_config(Path(__file__).parent.joinpath("example_config.yaml"))
    configured_fn(
        code_only="code_co",
        code_and_config="code_co_cf",
        code_and_cli="code_co_cl",
        code_config_and_cli="code_co_cf_cl",
    )
