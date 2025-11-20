from argparse import ArgumentParser
from inspect import signature
import logging

clog = logging.getLogger(__name__)
clover_parser = ArgumentParser()


def clover(fn):
    def overridden(*args, **kwargs):
        clog.debug(
            f"Calling function {fn.__qualname__} in module {fn.__module__} "
            f"with args={args} and kwargs={kwargs}"
        )

        spam = signature(fn).parameters
        param_names = spam.keys()
        clog.debug(f"Identified param names: {list(param_names)}")

        for pn in param_names:
            clover_parser.add_argument(f"--{fn.__qualname__}.{pn}")
        parsed_args = vars(clover_parser.parse_known_args()[0])
        clog.debug(f"Parsed the following args from cil: {parsed_args}")

        # dropping Nones for now but unclear how robust that is
        parsed_args = {
            k.rsplit(".", 1)[-1]: v
            for k, v in parsed_args.items()
            if (v is not None)
            and (k.rsplit(".", 1)[-1] in param_names)
            and (k.rsplit(".", 1)[0] == fn.__qualname__)
        }
        clog.debug(f"Sanitized parsed cli kwargs to: {parsed_args}")

        updated_args = dict(zip(param_names, args))
        updated_args.update(kwargs)
        updated_args.update(parsed_args)
        clog.debug(
            f"Forwarding the following (kw)args to wrapped function: {updated_args}"
        )

        return fn(**updated_args)

    return overridden
