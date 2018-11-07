def print_kwarg(**kwargs):
    print(kwargs.get(kwargs.get('key')))

print_kwarg(name="christian", key="k")