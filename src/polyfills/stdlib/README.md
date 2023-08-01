# Polyfills - `stdlib`

Backporting of some of the features natively available in newer Python versions:

- [**`bool`**](future_types/bool.py) class (as well as `True` and `False`)
- [**`sorted()`**](sorted.py) function
- [**`NotImplementedError`**](exceptions.py) exception (`Python 2.2`)

> For a quick one-time workaround for `True` and `False`:
>
> ```python
> exec("try: (True, False)\nexcept NameError: exec('True = 1==1; False = 1==0')")
> ```
