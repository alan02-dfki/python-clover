# python-clover
Clover - Command line override for python callables

## Example Requests

### Function vs Method
```bash
python -m clover.examples.function_vs_method \
  --module_function.overridden_arg foo \
  --module_function.overridden_kwarg bar \
  --Dog.__init__.name Spot \
  --Dog.bark.bark woof \
  --Dog.dig.burrow hole \
  --Dog.wag.body_part tail
```

### Type Casting
```bash
python -m clover.examples.type_casting \
  --type_casting.i 1 \
  --type_casting.l "[1, 2]" \
  --type_casting.s 1 \
  --type_casting.ani 1 \
  --type_casting.anl "[1, 2]" \
  --type_casting.andct "{'a':1, 'b':2}"
```

### Config File
When calling `clover.decorator.connect_config` with a path to a config file
in yaml format _all_ of its fields are converted to optional arguments
(regardless of whether they are used).
Then, when decorating a function or method with `@clover`,
values specified in this config file are substituted.

> [!IMPORTANT]
> The substitution priority is:<br>
> code < config < cli

Optional arguments obtained from a config file have default
values as specified in the config.
Refer to the file [example_config.yaml](clover/examples/example_config.yaml).
In particular, note, that in the config, too, the parameters are prefixed
with the full qualified name for the method or function they belong to.

You can run an [example script](clover/examples/config_parsing.py)
demonstrating this behavior with the following command:

```bash
python -m clover.examples.config_parsing \
  --configured_fn.cli_only "cli_cl" \
  --configured_fn.config_and_cli "cli_cf_cl" \
  --configured_fn.code_and_cli "cli_co_cl" \
  --configured_fn.code_config_and_cli "cli_co_cf_cl" \
  \
  --complex_type_cfg.list_from_cli "[0.1, 0.2, 0.3]" \
  --complex_type_cfg.list_from_cfg_overridden "[0.0001, 0.0002, 0.0003]"
```
