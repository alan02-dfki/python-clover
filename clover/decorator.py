from ast import literal_eval
from functools import wraps
from inspect import Parameter, signature
import logging
from pathlib import Path
from typing import Optional


from .parser import CloverParser

clog = logging.getLogger(__name__)


def _try_eval_literal(s, warn_arg_name: Optional[str] = None):
    warn_arg_name = warn_arg_name or s
    if isinstance(s, str):
        try:
            return literal_eval(s)
        except (ValueError, SyntaxError) as e:
            if str(e).startswith("malformed node or string") or str(e).startswith(
                "invalid decimal literal"
            ):
                clog.warning(
                    f"Faild to infer python type for arg {warn_arg_name} with value {s}; "
                    "Assuming type string."
                )
                return s
            else:
                raise e
    else:
        clog.debug(
            f"Skipping literal evaluation since {warn_arg_name} has type {type(s)}."
        )
        return s


def connect_config(config_path: str | Path):
    CloverParser.connect_config(config_path)


def clover(fn=None, *, alias: Optional[str] = None):
    def aliased(fn):
        @wraps(fn)
        def overridden(*args, **kwargs):
            if alias is None:
                identifier = fn.__qualname__
                clog.debug(
                    f"Calling function {fn.__qualname__} in module {fn.__module__} "
                    f"with args={args} and kwargs={kwargs}"
                )
            else:
                identifier = alias
                clog.debug(
                    f"Calling function {fn.__qualname__} in module {fn.__module__} "
                    f"aliased as {alias} with args={args} and kwargs={kwargs}"
                )

            clover_parser = CloverParser(id=identifier)
            spam = signature(fn).parameters
            param_names = spam.keys()
            clog.debug(f"Identified param names: {list(param_names)}")

            for pn in param_names:
                clover_parser.add_argument(pn)
            parsed_args = clover_parser.parse()
            clog.debug(f"Parsed the following args from cil: {parsed_args}")

            # dropping Nones for now but unclear how robust that is
            parsed_args = {
                k.rsplit(".", 1)[-1]: v
                for k, v in parsed_args.items()
                if (v is not None)
                and (k.rsplit(".", 1)[-1] in param_names)
                and (k.rsplit(".", 1)[0] == identifier)
            }
            clog.debug(f"Sanitized parsed cli kwargs to: {parsed_args}")

            for pname in parsed_args.keys():
                p = spam[pname]
                if (
                    (p.annotation != Parameter.empty and p.annotation != str)
                    or (
                        (p.default != Parameter.empty)
                        and (not isinstance(p.default, str))
                    )
                    or (pname in clover_parser.cfg_params)
                ):
                    parsed_args[pname] = _try_eval_literal(
                        parsed_args[pname], f"--{identifier}.{pname}"
                    )
            types = {k: type(v) for k, v in parsed_args.items()}
            clog.debug(f"Types after evaluation: {types}")

            updated_args = dict(zip(param_names, args))  # args passed at function call
            updated_args.update(kwargs)  # kwargs passed at function call
            updated_args.update(
                parsed_args
            )  # optargs from cli with defaults from config
            clog.debug(
                f"Forwarding the following (kw)args to wrapped function: {updated_args}"
            )
            return fn(**updated_args)

        return overridden

    if fn is not None:
        return aliased(fn)
    else:
        return aliased
