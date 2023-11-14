# Polyfills - `stdlib`

Backporting of some of the features natively available in newer Python versions:

- [**`bool`**](future_types/bool.py) class (as well as `True` and `False`)
- [**`sorted()`**](functions.py) function (`Python 2.4`)
- [**`sum()`**](functions.py) function (`Python 2.3`)
- [**`print()`**](print.py) function (keyword arguments such as `end` or `sep` were added in `Python 3.3`, see module docstring for more details)
- [**`NotImplementedError`**](exceptions.py) exception (`Python 2.2`)

> For a quick one-time workaround for `True` and `False`:
>
> ```python
> exec("try: (True, False)\nexcept NameError: exec('True = 1==1; False = 1==0')")
> ```
