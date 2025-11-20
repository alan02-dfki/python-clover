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
